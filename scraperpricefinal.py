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
from bs4 import BeautifulSoup
import os
from datetime import datetime

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
    
start = 0 # array position to start (inclusive)
end = 10000  # array position to end (exclusive)
# List of codes to process
codes = ['C00000601-A133', 'C00005812', 'C00005823', 'C00005824', 'C00005825', 'C00005826', 'C00005827', 'C00005828', 'C00005829', 'C00005830', 'C00005831', 'C00007943', 'C00007956', 'C00013593', 'C00015967', 'C00015968', 'C00027221-4100', 'C00027222-4100', 'C00032143', 'C00049276', 'C00060999', 'C00066424-4100', 'C00066425-4100', 'C00073043-bla', 'C00073043-blu', 'C00073043-gre', 'C00073044-bla', 'C00073044-blu', 'C00073044-gre', 'C00073045-bla', 'C00073045-blu', 'C00073045-gre', 'C00073046-bla', 'C00073046-blu', 'C00073046-gre', 'C00073636', 'C00075904', 'C00076660', 'C00076863', 'C00076901', 'C00076904', 'C00076977', 'C00076978', 'C00077048', 'C00077308', 'C00077309', 'C00077415', 'C00077440', 'C00077468', 'C00077562', 'C00077566', 'C00078351', 'C00078364-A131', 'C00078367-A131', 'C00079199', 'C00079498', 'C00080429', 'C00085503', 'C00085853', 'C00085854', 'C00085902', 'C00085913', 'C00085915', 'C00086253-4100', 'C00086286-4100', 'C00087356', 'C00088609', 'C00088988', 'C00088989', 'C00089053', 'C00094590', 'C00094656', 'C00096064-M001', 'C00096267', 'C00096268', 'C00097393-4100', 'C00097395-4100', 'C00097402-4100', 'C00097416-4100', 'C00097417-4100', 'C00097422-4100', 'C00097464-4100', 'C00097465-4100', 'C00097467-4100', 'C00097474-4100', 'C00097475-4100', 'C00097579-4100', 'C00098037-4100', 'C00098117-4100', 'C00098199-4100', 'C00098945', 'C00099102-4100', 'C00099103-4100', 'C00099347-4100', 'C00099376-4100', 'C00100405', 'C00100591', 'C00101826-4100', 'C00101866', 'C00102391', 'C00102581-4100', 'C00105336', 'C00105340', 'C00105979-4100', 'C00106878-4100', 'C00106879-4100', 'C00109185-4100', 'C00109186-4100', 'C00109668', 'C00110463-4100', 'C00111795', 'C00111805', 'C00112356-4100', 'C00112461-4100', 'C00114001', 'C00114002', 'C00116710-4100', 'C00117561', 'C00117852-4100', 'C00117991', 'C00117992', 'C00118081-F040', 'C00118087-2145', 'C00118088-2145', 'C00118100-2146', 'C00118101-2146', 'C00118331-4100', 'C00119821', 'C00125657', 'C00125658', 'C00125659', 'C00125662', 'C00125664', 'C00126338', 'C00126583', 'C00127784', 'C00127786', 'C00127787', 'C00127987', 'C00127988', 'C00130670', 'C00140546', 'C00144064', 'C00147511', 'C00147880', 'C00152772', 'C00154488-4100', 'C00154525', 'C00154783', 'C00156815', 'C00156822', 'C00157657', 'C00158727', 'C00158728', 'C00158729', 'C00158730', 'C00165650', 'C00173980-4100', 'C00191301-4100', 'C00191654', 'C00191655', 'C00196745', 'C00200268', 'C00200270', 'C00200521-4100', 'C00203234', 'C00211456', 'C00212336', 'C00217631', 'C00217633', 'C00218029', 'C00229321', 'C00229322', 'C00233394', 'C00235572-4100', 'C00236683', 'C00241088-4100', 'C00243060', 'C00243346', 'C00246092', 'C00247595', 'C00249122-4100', 'C00254216-4100', 'C00254221-4100', 'C00254952', 'C00254993-3016', 'C00255272', 'C00278696', 'C00278698', 'C00282644', 'C00283252-4100', 'C00304602-4100', 'C00307228', 'C00308206-4100', 'C00316771-4100', 'C00320137-4100', 'C00320138-4100', 'C00320142-4100', 'C00320143-4100', 'C00334165', 'C00446282', 'C00469711', 'C00471078', 'C00471087', 'C00521629', 'C00539863', 'C00539866', 'C00539867', 'C00543551-bla', 'C00543551-blu', 'C00543551-gre', 'C00570061', 'C00570065', 'C00585980', 'C00637484', 'C00642739', 'C00671899', 'C00678886', 'C00679772', 'C00690364', 'C00697791', 'C00704930', 'C00704931', 'C00704932', 'C00731552', 'C00744243', 'C00752821', 'C00888852']

def extract_whs_and_stock():
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find the exact match for the target row div
        target_div = soup.find("div", style=lambda s: s and
            "overflow: hidden" in s and
            "user-select: none" in s and
            "height: 19px" in s and
            "position: relative" in s and
            "z-index: 0" in s and
            "width: 1072px" in s and
            "border-bottom-color: transparent" in s)

        if not target_div:
            print("❌ Specific styled target row div not found.")
            return {}

        # Now find first two z-index: 3 divs inside
        z3_divs = target_div.find_all("div", style=lambda s: s and "z-index: 3" in s)
        if len(z3_divs) < 2:
            print("❌ Less than two z-index:3 divs found.")
            return {}

        whs_value = z3_divs[0].get_text(strip=True)
        stock_value = z3_divs[1].get_text(strip=True)

        return {
            "whs": whs_value,
            "stock_available": stock_value
        }

    except Exception as e:
        print(f"Error extracting WHS and stock: {e}")
        traceback.print_exc()
        return {}

# Create output folder named with date and time
output_folder = datetime.now().strftime("output_%Y%m%d_%H%M%S")
os.makedirs(output_folder, exist_ok=True)

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

    # Adjust end if it's out of range
    actual_end = end if end <= len(codes) else len(codes)
    selected_codes = codes[start:actual_end]
    for code in selected_codes:
        try:
            print(f"\nProcessing code: {code}")
            active_element = driver.switch_to.active_element
            active_element.clear()
            active_element.send_keys(code)
            active_element.send_keys(Keys.RETURN)

            print("Submitted. Waiting 5 seconds...")
            time.sleep(1)

            form_data = extract_all_form_values()
            extra_data = extract_whs_and_stock()

            if form_data:
                form_data['whs_stock'] = extra_data
                filename = os.path.join(output_folder, f"{code}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(form_data, f, indent=2, ensure_ascii=False)
                print(f"Saved to {filename}")
        except Exception as e:
            print(f"Error with code {code}: {e}")
            traceback.print_exc()
    print("✅ Finished processing selected codes.")

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
