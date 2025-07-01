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
codes = ["C00081696", "C00168948", "C00168950", "C00168949", "C00168951", "C00168953", "C00154168", "C00154169", "C00167156", 
"B00003511", "B00004762", "B00005330", "C00026278", "C00337351", "C00339339", "C00339340", "C00277602", "C00277603", "B00004906", "C00316733", "C00168955", "C00168956", "C00168957", "C00168958", "C00280449", "C00034840", "C00124519-L001", "C00149477", "C00149478", "C00034841", "C00034864", "C00034865", "C00034866", "C00034867", "C00166105", "C00166107", "B00004653", "B00004683", "C00059723", "C00053812", "C00053812", "C00065153", "B00005257", "C00124834", "C00167264", "C00145644", "C00145645", "C00145646", "C00145647", "C00124830", "C00124831", "B00004199", "B00004199", "B00004683", 
"B00004683", "B00005177", "C00053812", "C00053812", "B00004653", "C00004540", "C00059723", "C00124805", "C00218286", "C00249361", "C00249362", "C00059723", "C00059723", "C00065153", "C00018966", "C00092096", "C00278385", "C00019959", "C00138431", "B00004034", "C00494020", "C00325457", "B00005351", "C00055163", "B00004953", "C00888880", "C00888881", "C00888882", "C00306666", "C00564039", "C00564029", "C00564036", "C00564031", "C00564032", "C00564033", "C00564035", "C00564037", "C00564038", "C00564034", "C00564040", "C00564041", "C00564042", "C00564043", "C00564044", "C00564046", "B00005351", "C00055163", "B00004953", "C00888880", "C00888881", "C00888882", "C00306666", "C00205310", "C00396072", "C00396070", "B00004110", "C00097090", "C00395936", "C00260973", "C00254634", "C00272931", "C00316554", "C00281794", "C00304122", "C00084145", "C00101952", "C00094838", "B00004606", "C00199839", "C00199837", "C00094770", "B00003509", "C00084142", "C00077445", "C00084166", "C00084144", "C00100402", "C00100426", "C00321830", "B00004025", "B00004085", "B00004623", "C00233173", "C00364450", "C00428094", "C00047710", "C00205146", "C00004548", "C00165954-M001", "C00165953-M001", 
"C00065153", "C00083158", "C00167387", "C00167646", "C00124256", "B00005177", "B00004623", "C00385580-M001", "C00287425", "C00287426", "B00005251", "C00124694", "C00076595", "C00202823", "C00202824", "C00056659", "C00056660", "C00027370", "C00027367", "C00014021", "C00013590", "C00003413", "C00003415", "B00004653", "C00027374", "C00127570", "C00122258", "C00301137", "C00085605", "B00004085", "B00004085", "B00004303", "C00198458", "C00198457", "C00198459", "C00340263", "B00004623", "C00033625", "C00268860", "C00194011", "C00268862", "C00268859", "C00268861", "C00268857", "C00268855", 
"C00334115", "C00268854", "C00193999", "C00268856", "C00268858", "C00194010", "B00004035", "C00427675", "C00280653", "C00325643", "C00123785"]

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

            """ print("Submitted. Waiting 5 seconds...") """
            """ time.sleep() """

            form_data = extract_all_form_values()
            extra_data = extract_whs_and_stock()

            if form_data:
                combined_data = {
                    "form_data": form_data,
                    "whs_stock": extra_data
                }
                filename = f"{code}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(combined_data, f, indent=2, ensure_ascii=False)
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
