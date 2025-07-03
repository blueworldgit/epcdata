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
codes = ['B00004134', 'B00004852', 'B00005245', 'B00005365', 'B00005441', 'B00005895', 'C00001086', 'C00001088', 'C00001105', 'C00001668', 'C00001726', 'C00003453', 'C00008505', 'C00022597', 'C00026221-A133', 'C00032940', 'C00032961', 'C00050113', 'C00050116', 'C00050117', 'C00050118', 'C00050119', 'C00050121', 'C00050128', 'C00050132', 'C00050138', 'C00050141', 'C00050145', 'C00050150', 'C00050152', 'C00050153', 'C00050154', 'C00050157', 'C00050158', 'C00050160', 'C00050194', 'C00051438', 'C00051645', 'C00054387', 'C00054389', 'C00054390', 'C00054391', 'C00054392', 'C00054394', 'C00054396', 'C00054397', 'C00067600', 'C00073043-bla', 'C00073043-blu', 'C00073043-gre', 'C00073044-bla', 'C00073044-blu', 'C00073044-gre', 'C00073045-bla', 'C00073045-blu', 'C00073045-gre', 'C00073046-bla', 'C00073046-blu', 'C00073046-gre', 'C00073642', 'C00073643', 'C00076336', 'C00076523-A133', 'C00076527-A133', 'C00077048', 'C00077159', 'C00077218-A133', 'C00078396-A131', 'C00078397-A131', 'C00078443', 'C00078445', 'C00078718', 'C00079685', 'C00079817', 'C00080861-4100', 'C00080897-4100', 'C00080907-4100', 'C00080914-4100', 'C00081135-4100', 'C00081244', 'C00082201', 'C00083663', 'C00084280', 'C00085507', 'C00085629', 'C00085651', 'C00085984', 'C00085987', 'C00086104', 'C00086105', 'C00086835', 'C00086836', 'C00086837', 'C00086841', 'C00086842', 'C00086843', 'C00087169', 'C00087170', 'C00087172', 'C00087470', 'C00087471', 'C00087472', 'C00087618', 'C00087626', 'C00087628', 'C00087629', 'C00087632', 'C00087647', 'C00087648', 'C00087682', 'C00087866', 'C00088230', 'C00088231', 'C00088306', 'C00088388', 'C00088434-4100', 'C00088609', 'C00088978', 'C00089117-4100', 'C00089209', 'C00089700', 'C00090252-4100', 'C00092303', 'C00093085', 'C00094551', 'C00094552', 'C00094632', 'C00094991', 'C00095485', 'C00096307', 'C00096308', 'C00096309', 'C00096312', 'C00096388-4100', 'C00097243', 'C00097258', 'C00097349', 'C00097403-4100', 'C00097851', 'C00098097-4100', 'C00098141', 'C00098321', 'C00098322', 'C00099222', 'C00099624-4100', 'C00100005', 'C00100006', 'C00100427', 'C00100466', 'C00101622', 'C00101625', 'C00101627', 'C00101634', 'C00101644', 'C00101674', 'C00101827-4100', 'C00101867', 'C00101916', 'C00101923', 'C00101928', 'C00103044', 'C00103045', 'C00105000', 'C00105003', 'C00105004', 'C00105005', 'C00105191', 'C00106216-4100', 'C00106663', 'C00106664', 'C00108334', 'C00108335', 'C00108742-4100', 'C00109672', 'C00109697', 'C00109702', 'C00110079', 'C00113470', 'C00113582-4100', 'C00113643', 'C00113644', 'C00116553', 'C00116663', 'C00118694', 'C00118874', 'C00119242', 'C00123076', 'C00123079', 'C00130947', 'C00134345', 'C00134439', 'C00134447-4100', 'C00138387', 'C00144589', 'C00144867-A133', 'C00144870-A133', 'C00144876-A133', 'C00144884-A133', 'C00153841', 'C00154454', 'C00155256', 'C00155257', 'C00165647', 'C00169032', 'C00176667', 'C00176668', 'C00176669', 'C00184178', 'C00184472', 'C00185632', 'C00185716', 'C00185736', 'C00185763', 'C00186388', 'C00188126', 'C00192356', 'C00192755', 'C00193379', 'C00203233', 'C00206002', 'C00206602', 'C00206604', 'C00207451', 'C00210672', 'C00211249', 'C00213633', 'C00213849', 'C00213878', 'C00215485', 'C00215928', 'C00215929', 'C00216684', 'C00217987', 'C00218301', 'C00218477', 'C00219451', 'C00219452', 'C00224751', 'C00226800', 'C00227699', 'C00228953', 'C00228954', 'C00228955', 'C00228956', 'C00228957', 'C00228958', 'C00228983', 'C00228991', 'C00229310', 'C00233814', 'C00233815', 'C00235489', 'C00237251-4100', 'C00237252-4100', 'C00238310', 'C00243766-4100', 'C00245918', 'C00245919', 'C00245920', 'C00245922', 'C00245923', 'C00245924', 'C00245926', 'C00245927', 'C00245928', 'C00245929', 'C00245930', 'C00245932', 'C00245933', 'C00245934', 'C00245935', 'C00245937', 'C00245939', 'C00245940', 'C00245941', 'C00245942', 'C00245944', 'C00245945', 'C00245947', 'C00245951', 'C00245959', 'C00246008', 'C00246009', 'C00246010', 'C00246011', 'C00246012', 'C00246020', 'C00246022', 'C00246023', 'C00246024', 'C00246025', 'C00246063', 'C00246064', 'C00246065', 'C00246066', 'C00246068', 'C00246070', 'C00246072', 'C00246073', 'C00246078', 'C00246080', 'C00246081', 'C00246082', 'C00246083', 'C00246084', 'C00246086', 'C00246087', 'C00246089', 'C00246090', 'C00246091', 'C00246092', 'C00246093', 'C00246096', 'C00246098', 'C00246100', 'C00246102', 'C00246103', 'C00246104', 'C00246107', 'C00246108', 'C00246110', 'C00246112', 'C00246113', 'C00246114', 'C00246115', 'C00246116', 'C00246117', 'C00246118', 'C00246120', 'C00246121', 'C00246122', 'C00246123', 'C00246124', 'C00246125', 'C00246126', 'C00246127', 'C00246128', 'C00246129', 'C00246130', 'C00246131', 'C00246133', 'C00246134', 'C00246135', 'C00247000-4100', 'C00247383', 'C00247384', 'C00249229', 'C00249230', 'C00249244', 'C00249245', 'C00249247', 'C00249248', 'C00249249', 'C00256362', 'C00261167', 'C00261169', 'C00267744', 'C00268536', 'C00269996', 'C00270698', 'C00273085', 'C00274529', 'C00275612', 'C00275613', 'C00281639', 'C00283272', 'C00283475', 'C00287969', 'C00288079-A136', 'C00288080-A136', 'C00288665', 'C00293747', 'C00300183', 'C00304699', 'C00308722-4100', 'C00311675-4100', 'C00313789', 'C00314991', 'C00314993', 'C00316705', 'C00320156-4100', 'C00320157-4100', 'C00320325', 'C00322227', 'C00334137', 'C00334165', 'C00403865', 'C00446282', 'C00469711', 'C00471078', 'C00471087', 'C00521629', 'C00539863', 'C00539866', 'C00539867', 'C00542185', 'C00543551-bla', 'C00543551-blu', 'C00543551-gre', 'C00549131', 'C00566517', 'C00570061', 'C00570065', 'C00585980', 'C00614493', 'C00618313', 'C00618314', 'C00637484', 'C00642739', 'C00655134', 'C00671899', 'C00678886', 'C00679772', 'C00690364', 'C00697791', 'C00704930', 'C00704931', 'C00704932', 'C00731552', 'C00744243', 'C00752821', 'C00888852']

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
