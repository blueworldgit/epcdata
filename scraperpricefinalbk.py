from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pynput import keyboard
import time
import traceback
import json

# Initialize data storage
collected_html_sections = []
collected_form_data = []

# Set up browser (NOT headless so you can see and interact with it)
options = Options()
options.add_experimental_option("detach", True)  # Keeps browser open
driver = webdriver.Chrome(options=options)

# Navigate to login page
login_url = "https://xt.harrisgroup.ie/welcome"
driver.get(login_url)

# Store the original window handle for reference
original_window = driver.current_window_handle

# Prompt user to manually login
print("Please log in manually in the browser window...")

# Extract form data using JavaScript
def extract_all_form_values():
    try:
        form_data = driver.execute_script(""" 
            const allFormData = {
                timestamp: new Date().toISOString(),
                url: window.location.href,
                title: document.title,
                forms: [],
                allInputs: [],
                selectInputs: [],
                textareaInputs: []
            };

            const forms = document.querySelectorAll('form');
            forms.forEach((form, formIndex) => {
                const formInfo = {
                    formIndex: formIndex,
                    id: form.id,
                    name: form.name,
                    action: form.action,
                    method: form.method,
                    className: form.className,
                    fields: []
                };

                const formControls = form.querySelectorAll('input, select, textarea');
                formControls.forEach((control, controlIndex) => {
                    const fieldInfo = {
                        index: controlIndex,
                        tagName: control.tagName.toLowerCase(),
                        type: control.type || '',
                        name: control.name || '',
                        id: control.id || '',
                        className: control.className || '',
                        value: control.value || '',
                        checked: control.checked || false,
                        selected: control.selected || false,
                        disabled: control.disabled || false,
                        readonly: control.readOnly || false,
                        placeholder: control.placeholder || '',
                        maxLength: control.maxLength || null,
                        title: control.title || '',
                        'aria-label': control.getAttribute('aria-label') || '',
                        'data-tooltip': control.getAttribute('data-tooltip') || ''
                    };

                    if (control.tagName.toLowerCase() === 'select') {
                        fieldInfo.options = Array.from(control.options).map(option => ({
                            value: option.value,
                            text: option.text,
                            selected: option.selected
                        }));
                    }

                    formInfo.fields.push(fieldInfo);
                });

                allFormData.forms.push(formInfo);
            });

            const allInputs = document.querySelectorAll('input');
            allInputs.forEach((input, index) => {
                allFormData.allInputs.push({
                    index: index,
                    tagName: input.tagName.toLowerCase(),
                    type: input.type || '',
                    name: input.name || '',
                    id: input.id || '',
                    className: input.className || '',
                    value: input.value || '',
                    checked: input.checked || false,
                    disabled: input.disabled || false,
                    readonly: input.readOnly || false,
                    placeholder: input.placeholder || '',
                    maxLength: input.maxLength || null,
                    title: input.title || '',
                    'aria-label': input.getAttribute('aria-label') || '',
                    'data-tooltip': input.getAttribute('data-tooltip') || '',
                    outerHTML: input.outerHTML
                });
            });

            const allSelects = document.querySelectorAll('select');
            allSelects.forEach((select, index) => {
                allFormData.selectInputs.push({
                    index: index,
                    name: select.name || '',
                    id: select.id || '',
                    className: select.className || '',
                    value: select.value || '',
                    disabled: select.disabled || false,
                    title: select.title || '',
                    options: Array.from(select.options).map(option => ({
                        value: option.value,
                        text: option.text,
                        selected: option.selected
                    }))
                });
            });

            const allTextareas = document.querySelectorAll('textarea');
            allTextareas.forEach((textarea, index) => {
                allFormData.textareaInputs.push({
                    index: index,
                    name: textarea.name || '',
                    id: textarea.id || '',
                    className: textarea.className || '',
                    value: textarea.value || '',
                    disabled: textarea.disabled || false,
                    readonly: textarea.readOnly || false,
                    placeholder: textarea.placeholder || '',
                    title: textarea.title || ''
                });
            });

            return allFormData;
        """)
        collected_form_data.append(form_data)
        return form_data
    except Exception as e:
        print(f"Error extracting form values: {e}")
        traceback.print_exc()
        return None

# List of codes to process
codes = ["C00173421", "C00082271", "C00204388", "C00107138", "C00141745",
         "C00180125", "B00004097", "B00004878", "B00004151", "C00201990"]

def run_all_codes():
    print("Finding XT window...")

    xt_window = None
    all_windows = driver.window_handles

    for window_handle in all_windows:
        driver.switch_to.window(window_handle)
        if "XT" in driver.title:
            xt_window = window_handle
            print(f"Found XT window: {driver.title}")
            break

    if not xt_window:
        print("XT window not found.")
        return

    driver.switch_to.window(xt_window)

    for code in codes:
        try:
            print(f"\nProcessing code: {code}")
            active_element = driver.switch_to.active_element
            active_element.clear()
            active_element.send_keys(code)
            active_element.send_keys(Keys.RETURN)

            print("Submitted. Waiting 5 seconds...")
            time.sleep(5)

            form_data = extract_all_form_values()
            if form_data:
                filename = f"{code}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(form_data, f, indent=2, ensure_ascii=False)
                print(f"Saved to {filename}")
        except Exception as e:
            print(f"Error with code {code}: {e}")
            traceback.print_exc()

# Keyboard event handlers
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            if key.char.lower() == 'g':
                run_all_codes()
            elif key.char.lower() == 'q':
                print("\nQuitting and saving collected form data if any...")
                if collected_form_data:
                    with open("collected_form_data.json", "w", encoding="utf-8") as f:
                        json.dump(collected_form_data, f, indent=2, ensure_ascii=False)
                    print("Form data saved to 'collected_form_data.json'")
                driver.quit()
                return False
        elif key == keyboard.Key.enter:
            print("Enter key pressed (no action assigned).")
    except AttributeError:
        pass

input("Press Enter once you've logged in successfully...")

print("\n✅ Ready!")
print("→ Press 'g' to process all codes.")
print("→ Press 'q' to quit and save.")
print("Listening for keystrokes...")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
