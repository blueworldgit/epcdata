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
end = 600  # array position to end (exclusive)
# List of codes to process
codes = ['C00443100', 'C00112870', 'C00611168', 'C00544374', 'C00035127', 'C00014704', 'C00104358', 'C00071868', 'C00013851', 'C00112864', 'C00032700', 'C00026832', 'C00070569', 'C00013880', 'C00074850', 'C00050140', 'C00021124', 'C00001382', 'C00386117', 'C00090218', 'C00242759', 'C00211221', 'C00041591', 'C00013871', 'C00256386', 'C00215575', 'C00058304', 
'C00032976', 'C00089551', 'C00101165', 'C00005629', 'C00693811', 'C00026223', 'C00021127', 'C00650688', 'C00387916', 'C00054256', 'C00191101', 'C00625046', 'C00058642', 'C00005518', 'C00345241', 'C00016335', 'C00353290', 'C00534891', 'C00087061', 'C00002687', 'C00670099', 'C00553105', 'C00195706', 'C00074817', 'C00088651', 'C00138058', 'C00611172', 'C00215576', 'C00003836', 'B00005870', 'C00227583', 'C00014521', 'C00534894', 'C00051644', 'C00342320', 'C00076674', 'C00216803', 'C00210713', 'C00043498', 'C00049667', 'C00021121', 'C00670102', 'C00267328', 'C00437266', 'C00112280', 'C00040829', 'C00313998', 'C00016192', 'C00001366', 'C00130750', 'C00270786', 'C00015165', 'C00016352', 'C00392577', 'C00652857', 'C00037490', 'C00090215', 'C00312777', 'C00364389', 'C00517855', '99000066', 'C00126829', 'C00088639', 'C00088645', 'B00004763', 'C00065768', 'C00556124', 'C00275280', 'C00042720', 'C00098462', 'C00145323', 'C00014604', 'C00002688', 'C00016157', 'C00001372', 'C00216414', 'C00343587', 'C00090188', 'C00089548', 'C00006099', 'C00013841', 'B00005191', 'C00090209', 'C00145322', 'C00104418', 'C00346074', 'C00412803', 'C00419336', 'C00066713', 'C00145320', 'C00286028', 'C00034134', 'C00670096', 'C00028857', 'C00090174', 'C00218647', 'C00561192', 'C00026554', 'C00232777', 'B00005189', 'C00024700', 'C00014606', 'C00429707', 'C00088641', 'C00773820', 'C00090216', 'C00119688', 'C00038059', 'C00611174', 'C00015334', 'C00437184', 'C00098783', 'C00054257', 'C00016212', 'C00090185', 'C00024797', 'C00216410', 'C00216070', 'C00112408', 'C00050115', 'C00088643', 'C00689411', 'C00032375', 'C00342322', 'C00058223', 'C00191100', 'C00024562', 'C00085993', 'C00270785', 'C00111505', 'C00270895', 'C00070567', 'C00014416', 'C00006746', 'C00216412', 'C00013584', 'C00013582', 'C00255489', 'C00014832', 'B00004124', 'C00007847', 'C00005622', 'C00437685', 'C00478943', 'C00343612', 'C00065767', 'C00021129', 'C00689412', 'C00036083', 'C00211081', 'C00054255', 'C00145319', 'C00112869', 'C00016336', 'C00130749', 'C00216801', 'C00625038', 
'C00112866', 'C00033353', 'C00166355', 'C00067854', 'C00326208', 'C00112319', 'C00364385', 'C00693820', 'C00275285', 'C00342324', 'C00021120', 'C00045813', 'C00089249', 'C00085377', 'C00090206', 'C00002383', 'C00041057', 'C00065790', 'C00336210', 'C00317198', 'C00028550', 'C00218005', 'C00255023', 'C00006451', 'C00016200', 'C00104417', 'C00090128', 'C00035125', 'C00690387', 'C00216802', 'C00211083', 'C00216413', 'C00693818', 'C00004321', 'C00086078', 'C00024701', 'C00090201', 'C00089544', 'C00021123', 'C00567380', 'C00054393', 'C00016193', 'C00216416', 'C00006098', 'C00317904', 'C00514312', 'C00441392', 'C00089547', 'C00112840', 'C00106157', 'C00074560', 'C00078305', 'C00093389', 'C00693816', 'C00176194', 'C00218656', 'C00021122', 'C00421415', 'C00611176', 'C00006651', 'C00130738', 'C00312771', 'C00066900', 'C00024762', 'C00086261', 'C00313417', 'C00085992', 'C00024575', 'C00002860', 'C00005442', 'C00014555', 'C00479858', 'C00002304', 'C00088941', 'C00035932', 'C00104361', 'C00246092', 'C00045814', 'C00029243', 'C00022730', 'C00016197', 'C00016195', 'C00326217', 'C00089493', 'C00014664', 'C00625052', 'C00321092', 'C00342325', 'C00020770', 'C00032977', 'C00089491', 'C00014421', 'C00037492', 'C00089555', 'C00120933', 'C00021125', 'C00022555', 'C00089553', 'C00341407', 'C00321533', 'B00006053', 'C00190169', 'C00319019', 'C00015129', 'C00693819', 'C00670100', 'C00024747', 'C00670103', 'C00693817', 'C00320274', 'C00013583', 'C00090200', 'C00112865', 'C00313577', 'C00016271', 'C00437178']

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

# Create non-matches filename with date
nonmatches_filename = datetime.now().strftime("nonmatches_%Y%m%d_%H%M%S.txt")

def verify_correct_code_displayed(expected_code):
    """Verify that the correct code is displayed in the input field after submission"""
    try:
        # Check the active input element
        active_element = driver.switch_to.active_element
        current_value = active_element.get_attribute('value')
        
        if current_value == expected_code:
            return True, current_value
        else:
            print(f"⚠️  CODE MISMATCH: Expected '{expected_code}', but found '{current_value}'")
            return False, current_value
            
    except Exception as e:
        print(f"Error verifying code: {e}")
        return False, "ERROR"

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
    
    # Track statistics
    successful_codes = []
    mismatched_codes = []
    error_codes = []
    
    for code in selected_codes:
        try:
            print(f"\nProcessing code: {code}")
            active_element = driver.switch_to.active_element
            active_element.clear()
            active_element.send_keys(code)
            active_element.send_keys(Keys.RETURN)

            print("Submitted. Waiting for response...")
            time.sleep(2)

            # Verify the correct code is displayed
            is_correct, displayed_code = verify_correct_code_displayed(code)
            
            if is_correct:
                print(f"✅ Code verified: {displayed_code}")
                
                form_data = extract_all_form_values()
                extra_data = extract_whs_and_stock()

                if form_data:
                    form_data['whs_stock'] = extra_data
                    form_data['verified_code'] = displayed_code
                    form_data['original_search_code'] = code
                    
                    filename = os.path.join(output_folder, f"{code}.json")
                    with open(filename, "w", encoding="utf-8") as f:
                        json.dump(form_data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Saved verified data to {filename}")
                    successful_codes.append(code)
                else:
                    print(f"❌ No form data extracted for {code}")
                    error_codes.append(code)
            else:
                print(f"❌ SKIPPING: Code mismatch for {code} (got {displayed_code})")
                mismatched_codes.append({'searched': code, 'found': displayed_code})
                
                # Save mismatch info for reference
                mismatch_data = {
                    'original_search_code': code,
                    'displayed_code': displayed_code,
                    'status': 'CODE_MISMATCH',
                    'timestamp': datetime.now().isoformat()
                }
                filename = os.path.join(output_folder, f"{code}_MISMATCH.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(mismatch_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Error with code {code}: {e}")
            error_codes.append(code)
            traceback.print_exc()
    
    # Save non-matches to dated file
    if mismatched_codes:
        nonmatches_path = os.path.join(output_folder, nonmatches_filename)
        with open(nonmatches_path, "w", encoding="utf-8") as f:
            f.write(f"NON-MATCHING CODES REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total non-matches: {len(mismatched_codes)}\n")
            f.write(f"{'='*60}\n\n")
            
            for i, mismatch in enumerate(mismatched_codes, 1):
                f.write(f"{i:3d}. Searched: {mismatch['searched']:<15} → Found: {mismatch['found']}\n")
            
            f.write(f"\n{'='*60}\n")
            f.write(f"Summary: {len(mismatched_codes)} codes did not match exactly\n")
            f.write(f"These codes may need manual review or correction\n")
        
        print(f"💾 Non-matches saved to: {nonmatches_path}")
    
    # Print summary
    print(f"\n📊 PROCESSING SUMMARY:")
    print(f"   ✅ Successful: {len(successful_codes)}")
    print(f"   ⚠️  Code mismatches: {len(mismatched_codes)}")
    print(f"   ❌ Errors: {len(error_codes)}")
    
    if mismatched_codes:
        print(f"\n⚠️  MISMATCHED CODES (first 5):")
        for mismatch in mismatched_codes[:5]:  # Show first 5
            print(f"   {mismatch['searched']} → {mismatch['found']}")
        if len(mismatched_codes) > 5:
            print(f"   ... and {len(mismatched_codes) - 5} more (see {nonmatches_filename})")
    
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
