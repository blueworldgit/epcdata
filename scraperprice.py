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
login_url = "https://xt.harrisgroup.ie/welcome"  # Replace with your actual login URL
driver.get(login_url)

# Store the original window handle for reference
original_window = driver.current_window_handle

# Prompt user to manually login
print("Please log in manually in the browser window...")

# Function to extract all form values from the page
def extract_all_form_values():
    """Extract all form field values using JavaScript properties"""
    print("Extracting all form values from the page...")
    
    try:
        # Get all form data using JavaScript
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
            
            // Get all forms and their fields
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
                
                // Get all form controls within this form
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
                    
                    // For select elements, get all options
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
            
            // Also get ALL inputs on the page (even outside forms)
            const allInputs = document.querySelectorAll('input');
            allInputs.forEach((input, index) => {
                const inputInfo = {
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
                };
                allFormData.allInputs.push(inputInfo);
            });
            
            // Get all select elements
            const allSelects = document.querySelectorAll('select');
            allSelects.forEach((select, index) => {
                const selectInfo = {
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
                };
                allFormData.selectInputs.push(selectInfo);
            });
            
            // Get all textarea elements
            const allTextareas = document.querySelectorAll('textarea');
            allTextareas.forEach((textarea, index) => {
                const textareaInfo = {
                    index: index,
                    name: textarea.name || '',
                    id: textarea.id || '',
                    className: textarea.className || '',
                    value: textarea.value || '',
                    disabled: textarea.disabled || false,
                    readonly: textarea.readOnly || false,
                    placeholder: textarea.placeholder || '',
                    title: textarea.title || ''
                };
                allFormData.textareaInputs.push(textareaInfo);
            });
            
            return allFormData;
        """)
        
        # Print summary
        print("\n" + "="*60)
        print("FORM DATA EXTRACTION SUMMARY")
        print("="*60)
        print(f"URL: {form_data['url']}")
        print(f"Title: {form_data['title']}")
        print(f"Timestamp: {form_data['timestamp']}")
        print(f"Total Forms: {len(form_data['forms'])}")
        print(f"Total Inputs: {len(form_data['allInputs'])}")
        print(f"Total Selects: {len(form_data['selectInputs'])}")
        print(f"Total Textareas: {len(form_data['textareaInputs'])}")
        print("="*60)
        
        # Print detailed form information
        for form_idx, form in enumerate(form_data['forms']):
            print(f"\nFORM {form_idx + 1}:")
            print(f"  ID: {form['id']}")
            print(f"  Name: {form['name']}")
            print(f"  Action: {form['action']}")
            print(f"  Method: {form['method']}")
            print(f"  Fields in form: {len(form['fields'])}")
            
            for field_idx, field in enumerate(form['fields']):
                if field['value']:  # Only show fields with values
                    print(f"    Field {field_idx + 1}: {field['tagName']}")
                    print(f"      Name: {field['name']}")
                    print(f"      ID: {field['id']}")
                    print(f"      Type: {field['type']}")
                    print(f"      Value: '{field['value']}'")
                    print(f"      Readonly: {field['readonly']}")
                    print(f"      Title/Tooltip: {field['title']}")
                    if field['data-tooltip']:
                        print(f"      Data-tooltip: {field['data-tooltip']}")
                    print()
        
        # Print all inputs (including those outside forms)
        print("\nALL INPUTS WITH VALUES:")
        print("-"*40)
        for idx, input_info in enumerate(form_data['allInputs']):
            if input_info['value']:  # Only show inputs with values
                print(f"Input {idx + 1}:")
                print(f"  Name: {input_info['name']}")
                print(f"  ID: {input_info['id']}")
                print(f"  Type: {input_info['type']}")
                print(f"  Value: '{input_info['value']}'")
                print(f"  Readonly: {input_info['readonly']}")
                print(f"  Title: {input_info['title']}")
                print(f"  Class: {input_info['className']}")
                if 'PRC' in input_info['title'] or 'PRC' in input_info.get('data-tooltip', ''):
                    print(f"  *** SPECIAL: Contains PRC reference ***")
                print()
        
        # Store the form data
        collected_form_data.append(form_data)
        
        return form_data
        
    except Exception as e:
        print(f"Error extracting form values: {e}")
        traceback.print_exc()
        return None

# Modified input handler to find XT window and type "ABCD"
def handle_enter_input():
    """Finds window with 'XT' in title, types 'C00120184' and presses Enter"""
    print("Looking for window with 'XT' in title...")
    
    # Get all window handles
    all_windows = driver.window_handles
    
    # Find window with "XT" in title
    xt_window = None
    current_window = driver.current_window_handle
    
    for window_handle in all_windows:
        driver.switch_to.window(window_handle)
        window_title = driver.title
        if "XT" in window_title:
            xt_window = window_handle
            print(f"Found XT window: '{window_title}' (handle: {window_handle})")
            break
    
    if xt_window:
        # Make sure we're on the XT window
        driver.switch_to.window(xt_window)
        
        try:
            # Find the active element (or you can specify a particular input field)
            active_element = driver.switch_to.active_element
            
            # Type "C00120184" into the active element
            active_element.send_keys("C00120184")
            
            # Press Enter
            active_element.send_keys(Keys.RETURN)
            
            print("Typed 'C00120184' and pressed Enter in XT window")
            
            # Wait 3 seconds for the page to load/update
            print("Waiting 3 seconds for page to load...")
            time.sleep(3)
            
            # Extract all form values
            form_data = extract_all_form_values()
            
        except Exception as e:
            print(f"Error typing text in XT window: {e}")
            traceback.print_exc()
    else:
        print("No window with 'XT' in title found.")
        # List all available windows for debugging
        print("Available windows:")
        for i, window_handle in enumerate(all_windows):
            driver.switch_to.window(window_handle)
            print(f"  {i}: '{driver.title}' (handle: {window_handle})")
        
        # Switch back to original window if needed
        if current_window in all_windows:
            driver.switch_to.window(current_window)

# Wait for user login with Enter simulation
input("Press Enter when you've logged in successfully...")
handle_enter_input()

print("Login successful! Now you can navigate the site.")
print("- Press 's' to find window with 'XT' in title, enter 'C00120184', and extract form values")
print("- Press 'd' to debug page elements")
print("- Press 'e' to extract form values from current page")
print("- Press Enter to find window with 'XT' in title and type 'C00120184' + Enter")
print("- Press 'q' to save all data and quit the script")

# Function to save current page section with XT window detection
def save_current_page():
    print("Looking for window with 'XT' in title...")
    
    # Get all window handles
    all_windows = driver.window_handles
    
    # Find window with "XT" in title
    xt_window = None
    current_window = driver.current_window_handle
    
    for window_handle in all_windows:
        driver.switch_to.window(window_handle)
        window_title = driver.title
        if "XT" in window_title:
            xt_window = window_handle
            print(f"Found XT window: '{window_title}' (handle: {window_handle})")
            break
    
    if xt_window:
        # Make sure we're on the XT window
        driver.switch_to.window(xt_window)
        
        # Enter 'C00120184' and submit
        try:
            # Find the active element (or you can specify a particular input field)
            active_element = driver.switch_to.active_element
            
            # Type "C00120184" into the active element
            active_element.send_keys("C00120184")
            
            # Press Enter
            active_element.send_keys(Keys.RETURN)
            
            print("Typed 'C00120184' and pressed Enter in XT window")
            
            # Wait 3 seconds for the page to load/update
            print("Waiting 3 seconds for page to load...")
            time.sleep(3)
            
            # Extract all form values
            form_data = extract_all_form_values()
            
            # Get the full HTML content
            html_content = driver.page_source
            
            # Store HTML content in collected sections
            collected_html_sections.append(html_content)
                
        except Exception as e:
            print(f"Error entering text or getting content: {e}")
            traceback.print_exc()
    else:
        print("No window with 'XT' in title found.")
        # List all available windows for debugging
        print("Available windows:")
        for i, window_handle in enumerate(all_windows):
            driver.switch_to.window(window_handle)
            print(f"  {i}: '{driver.title}' (handle: {window_handle})")
        
        # Switch back to original window if needed
        if current_window in all_windows:
            driver.switch_to.window(current_window)

# Function to debug page elements
def debug_page():
    print("Current window info:")
    print(f"- Title: {driver.title}")
    print(f"- URL: {driver.current_url}")
    print(f"- Window handle: {driver.current_window_handle}")
    print(f"- Total windows open: {len(driver.window_handles)}")
    
    # List all windows
    for i, handle in enumerate(driver.window_handles):
        driver.switch_to.window(handle)
        print(f"  Window {i}: {driver.title} ({handle})")
    
    # Switch back to most recent popup or original window
    save_current_page()

# Function to extract form values from current page
def extract_current_page_values():
    print("Extracting form values from current page...")
    extract_all_form_values()

# Keyboard event handlers
def on_press(key):
    try:
        if hasattr(key, 'char') and key.char:
            if key.char.lower() == 's':
                save_current_page()
            elif key.char.lower() == 'd':
                debug_page()
            elif key.char.lower() == 'e':
                extract_current_page_values()
            elif key.char.lower() == 'q':
                print("\nSaving all collected data...")
                print(f"Total HTML sections collected: {len(collected_html_sections)}")
                print(f"Total form data snapshots collected: {len(collected_form_data)}")
                
                # Save HTML to file
                if collected_html_sections:
                    with open("collected_sections.html", "w", encoding="utf-8") as f:
                        for i, section in enumerate(collected_html_sections):
                            f.write(f"<!-- Section {i+1} -->\n")
                            f.write(section)
                            f.write("\n\n")
                    print("HTML data saved to 'collected_sections.html'")
                
                # Save form data to JSON file
                if collected_form_data:
                    with open("collected_form_data.json", "w", encoding="utf-8") as f:
                        json.dump(collected_form_data, f, indent=2, ensure_ascii=False)
                    print("Form data saved to 'collected_form_data.json'")
                
                # Clean up
                driver.quit()
                return False  # Stop listener
        elif key == keyboard.Key.enter:
            handle_enter_input()
    except AttributeError:
        pass

# Start keyboard listener
print("Keyboard listener started. Use 's', 'd', 'e', or 'q' keys...")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()