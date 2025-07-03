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
codes = ['B00003514', 'B00004020', 'B00004031', 'B00004096', 'B00004101', 'B00004105', 'B00004111', 'B00004128', 'B00004137', 'B00004152', 'B00004209', 'B00004455', 'B00004624', 'B00004682', 'B00004748', 'B00004793', 'B00004845', 'B00004878', 'B00004938', 'B00005001', 'B00005206', 'B00005233', 'B00005235', 'B00005249', 'B00005355', 'B00005372', 'B00005378', 'B00005391', 'B00005412', 'B00005501', 'B00005677', 'B00005783', 'B00005789', 'B00005828', 'C00001115', 'C00002521', 'C00002522', 'C00002524', 'C00002525', 'C00002785', 'C00002828', 'C00003529', 'C00003839', 'C00004052', 'C00004642', 'C00005814', 'C00005815', 'C00005816', 'C00005817', 'C00005818', 'C00005819', 'C00005820', 'C00005821', 'C00005822', 'C00005935', 'C00006353', 'C00008711', 'C00010097', 'C00013191', 'C00013586', 'C00015981', 'C00015982', 'C00016706', 'C00017856', 'C00017857', 'C00020183', 'C00023898', 'C00025126', 'C00027574', 'C00030135-4100', 'C00030141-4100', 'C00030142-4100', 'C00034711', 'C00034712', 'C00037326', 'C00039810', 'C00042013', 'C00042678', 'C00043556-4100', 'C00043557-4100', 'C00044727', 'C00045073', 'C00048008', 'C00049982-4100', 'C00049983-4100', 'C00050526', 'C00050648', 'C00051001', 'C00051007', 'C00053986', 'C00054221', 'C00055807', 'C00056425', 'C00058388-4100', 'C00060951', 'C00061106', 'C00062401', 'C00063297', 'C00064034', 'C00068478', 'C00069211', 'C00073043-bla', 'C00073043-blu', 'C00073043-gre', 'C00073044-bla', 'C00073044-blu', 'C00073044-gre', 'C00073045-bla', 'C00073045-blu', 'C00073045-gre', 'C00073046-bla', 'C00073046-blu', 'C00073046-gre', 'C00073633', 'C00073635', 'C00073637', 'C00073987', 'C00073990', 'C00073991', 'C00074178', 'C00074198', 'C00074203', 'C00074245', 'C00074418', 'C00074421', 'C00074523', 'C00074525', 'C00074527', 'C00074533', 'C00074534', 'C00074543', 'C00074544', 'C00074547', 'C00074572', 'C00074582', 'C00074583', 'C00074793', 'C00074798', 'C00074813', 'C00074835', 'C00075385', 'C00075413', 'C00075414', 'C00075415', 'C00075443', 'C00075450', 'C00075451', 'C00075461', 'C00075464', 'C00075683', 'C00075684', 'C00075685', 'C00075686', 'C00075687', 'C00075688', 'C00075693', 'C00075888', 'C00075892', 'C00075893', 'C00075902', 'C00075940', 'C00076123-A007', 'C00076125-F014', 'C00076148', 'C00076267', 'C00076347', 'C00076354', 'C00076420', 'C00076421', 'C00076422', 'C00076493', 'C00076592', 'C00076593', 'C00076594', 'C00076596', 'C00076597', 'C00076598', 'C00076599', 'C00076601', 'C00076602', 'C00076603', 'C00076604', 'C00076608', 'C00076609', 'C00076611', 'C00076620', 'C00076621', 'C00076622', 'C00076624', 'C00076625', 'C00076628', 'C00076629', 'C00076630', 'C00076631', 'C00076640', 'C00076641', 'C00076646', 'C00076652', 'C00076657', 'C00076658', 'C00076659', 'C00076661', 'C00076668', 'C00076675', 'C00076677', 'C00076678', 'C00076679', 'C00076699-4100', 'C00076704-4100', 'C00076714-4100', 'C00076721-4100', 'C00076723', 'C00076726-4100', 'C00076727', 'C00076739', 'C00076740-4100', 'C00076745-4100', 'C00076746-4100', 'C00076751-4100', 'C00076753-4100', 'C00076760-4100', 'C00076767', 'C00076796-4100', 'C00076799-4100', 'C00076800-4100', 'C00076809-4100', 'C00076810-4100', 'C00076817-4100', 'C00076827', 'C00076828', 'C00076861', 'C00076862', 'C00076874', 'C00076885', 'C00076886', 'C00076889', 'C00076890', 'C00076891', 'C00076893', 'C00076900', 'C00076903', 'C00076911', 'C00076912', 'C00076983', 'C00076984', 'C00076987', 'C00077002-4100', 'C00077016-4100', 'C00077034-4100', 'C00077035-4100', 'C00077040-4100', 'C00077048', 'C00077050', 'C00077158', 'C00077160', 'C00077161', 'C00077163', 'C00077171', 'C00077174', 'C00077176', 'C00077189', 'C00077192', 'C00077193', 'C00077194', 'C00077195', 'C00077196', 'C00077223', 'C00077230', 'C00077236', 'C00077333', 'C00077334', 'C00077402', 'C00077406', 'C00077411', 'C00077412', 'C00077433-A133', 'C00077444', 'C00077451', 'C00077453', 'C00077465', 'C00077532', 'C00077563', 'C00077564', 'C00077565', 'C00077641-4100', 'C00077661-4100', 'C00078304', 'C00078353', 'C00078369', 'C00078379-A132', 'C00078379-F050', 'C00078389-A132', 'C00078389-F050', 'C00078401', 'C00078402', 'C00078418-A131', 'C00078419-A131', 'C00078450-4100', 'C00078506-4100', 'C00078507-4100', 'C00078508-4100', 'C00078509-4100', 'C00078928-4100', 'C00079658', 'C00080085', 'C00080884-4100', 'C00081037-4100', 'C00081130-4100', 'C00081442', 'C00081713-4100', 'C00083490', 'C00083526', 'C00083527', 'C00083957', 'C00085341', 'C00085392', 'C00085393', 'C00085399', 'C00085400', 'C00085403', 'C00085404', 'C00085405', 'C00085455-4100', 'C00085456-4100', 'C00085493', 'C00085524', 'C00085529', 'C00085531', 'C00085564', 'C00085565', 'C00085566', 'C00085567', 'C00085696', 'C00085802', 'C00085815', 'C00085817', 'C00085818', 'C00085835', 'C00085855', 'C00085856', 'C00085857', 'C00085858', 'C00085859', 'C00085863', 'C00085877', 'C00085883', 'C00085884', 'C00085885', 'C00085886', 'C00085887', 'C00085891', 'C00085893', 'C00085904', 'C00085907', 'C00085908', 'C00085910', 'C00085911', 'C00085912', 'C00085914', 'C00085916', 'C00085917', 'C00085919', 'C00085920', 'C00085921', 'C00085924', 'C00085927', 'C00085963', 'C00085964', 'C00085965', 'C00085966', 'C00085967', 'C00086359', 'C00086365', 'C00086385', 'C00086391', 'C00086415', 'C00086777', 'C00086910-4100', 'C00086911-4100', 'C00087026-4100', 'C00087038-4100', 'C00087402', 'C00087585-4100', 'C00087644', 'C00087658-4100', 'C00087670-4100', 'C00087800', 'C00087988', 'C00088609', 'C00088887', 'C00089220', 'C00089389', 'C00089683', 'C00090120-4100', 'C00090127', 'C00090654-4100', 'C00090687-4100', 'C00091221-4100', 'C00091382-4100', 'C00091385-4100', 'C00092139', 'C00092437', 'C00092929', 'C00093293', 'C00094051', 'C00094056', 'C00094057', 'C00094244', 'C00094317', 'C00094330', 'C00094333', 'C00094439', 'C00094575', 'C00094588', 'C00094630', 'C00094668', 'C00094669', 'C00094672', 'C00094674', 'C00095202-4100', 'C00095413', 'C00095414', 'C00095415', 'C00095601', 'C00095631', 'C00096064', 'C00096313', 'C00097009', 'C00097277', 'C00097278', 'C00097522-4100', 'C00097606-4100', 'C00097607-4100', 'C00097750-4100', 'C00097786', 'C00097839', 'C00097852', 'C00098145-4100', 'C00098226', 'C00099024-4100', 'C00099276-4100', 'C00099277-4100', 'C00099345-4100', 'C00099372-4100', 'C00099635-4100', 'C00100013', 'C00100187-A136', 'C00100189-A136', 'C00100195', 'C00100202-A126', 'C00100209-A126', 'C00100334', 'C00100423', 'C00100592', 'C00100797-4100', 'C00100798-4100', 'C00101703', 'C00101827-4100', 'C00101830', 'C00101920', 'C00102154', 'C00102212', 'C00102245', 'C00102746', 'C00103271', 'C00103402', 'C00103428', 'C00103546', 'C00103630', 'C00103822', 'C00103823', 'C00104005', 'C00104386', 'C00105076', 'C00105102', 'C00105105', 'C00105277', 'C00105548', 'C00105549', 'C00105550', 'C00105782', 'C00105825-4100', 'C00105977-4100', 'C00105978-4100', 'C00105997', 'C00106835-4100', 'C00106909', 'C00106920', 'C00107172-4100', 'C00107304-4100', 'C00107339', 'C00107738', 'C00107739', 'C00107801-4100', 'C00107926-4100', 'C00108300', 'C00108694', 'C00108752', 'C00108753-A133', 'C00108753-F060', 'C00109671', 'C00109700', 'C00109701', 'C00110318', 'C00110325', 'C00111228', 'C00111232', 'C00111779', 'C00111791', 'C00112280-F014', 'C00112284', 'C00112285', 'C00112288-F014', 'C00112350-4100', 'C00112353-4100', 'C00112355-4100', 'C00112745', 'C00112991', 'C00112996', 'C00113098-4100', 'C00113465', 'C00113479', 'C00113645', 'C00113646', 'C00113728-A134', 'C00113808', 'C00113809', 'C00116865-4100', 'C00117030', 'C00117581', 'C00117582', 'C00117850-4100', 'C00118080', 'C00118081-F142', 'C00118087-2144', 'C00118088-2144', 'C00118089', 'C00118092', 'C00118098-A126', 'C00118099-A126', 'C00118100-F067', 'C00118101-F067', 'C00118102', 'C00118107-A126', 'C00118329-4100', 'C00118375', 'C00118988-4100', 'C00119012', 'C00119016', 'C00119161', 'C00119508', 'C00120456', 'C00120457', 'C00120535-4100', 'C00120691', 'C00121429', 'C00121533', 'C00121534', 'C00122529-4100', 'C00122541-4100', 'C00123939', 'C00125959', 'C00126071-4100', 'C00126383', 'C00127741', 'C00130035', 'C00130100', 'C00134445-4100', 'C00134931', 'C00134932', 'C00136459', 'C00136460', 'C00137544', 'C00137669', 'C00137677-A133', 'C00137677-F060', 'C00138368-4100', 'C00138369-4100', 'C00138380-4100', 'C00138382', 'C00138592', 'C00138593', 'C00140364', 'C00140528', 'C00141395-A133', 'C00141889', 'C00142276', 'C00143480', 'C00143482', 'C00143826', 'C00144066', 'C00145023', 'C00146573', 'C00147133', 'C00147636', 'C00147638', 'C00152957', 'C00154733', 'C00155286', 'C00157944', 'C00157945', 'C00158725', 'C00158726', 'C00165301', 'C00165302', 'C00165303', 'C00165304', 'C00165307', 'C00165308', 'C00165665', 'C00166147', 'C00173622', 'C00173629', 'C00173974-4100', 'C00175249', 'C00175250', 'C00176145', 'C00176147', 'C00180814', 'C00181734', 'C00182324-4100', 'C00183602', 'C00184621', 'C00184643', 'C00184646', 'C00185421', 'C00185422', 'C00188950', 'C00189354-4100', 'C00189355-4100', 'C00191865', 'C00191866', 'C00192366', 'C00193190', 'C00193242-4100', '', 'C00193380', 'C00195712-F060', 'C00196746', 'C00199742-4100', 'C00200137-4100', 'C00200138-4100', 'C00202409', 'C00204025-4100', 'C00204030-4100', 'C00204066', 'C00204067', 'C00206587', 'C00206905', 'C00207343', 'C00207961-F014', 'C00207962-F014', 'C00209969', 'C00210106', 'C00210490-F014', 'C00210491-F014', 'C00211013-M020', 'C00211104', 'C00211105', 'C00211110', 'C00211114', 'C00211393', 'C00211397', 'C00211486-A126', 'C00211490', 'C00211493', 'C00211494', 'C00211498', 'C00211499', 'C00212072', 'C00212331', 'C00212539', 'C00212540', 'C00212541', 'C00212542', 'C00212543', 'C00212550', 'C00212551', 'C00212552', 'C00213332', 'C00213912', 'C00213915', 'C00215065', 'C00215076', 'C00215078', 'C00215080', 'C00215118', 'C00215175', 'C00215177', 'C00215312', 'C00215314', 'C00215315', 'C00215316', 'C00215317', 'C00215318', 'C00215319', 'C00215320', 'C00215321', 'C00215322', 'C00215323', 'C00215324', 'C00215325', 'C00215326', 'C00215327', 'C00215328', 'C00215415', 'C00215926', 'C00215927', 'C00216402-A061', 'C00216406', 'C00216408', 'C00216409', 'C00216411', 'C00216415', 'C00216417-A061', 'C00216465', 'C00217255', 'C00218023', 'C00218026', 'C00218030', 'C00218114', 'C00218115', 'C00218376', 'C00218377', 'C00219058', 'C00219059', 'C00219061', 'C00219062', 'C00219063', 'C00219064', 'C00219065', 'C00220657', 'C00220660', 'C00220664', 'C00220665', 'C00220685', 'C00220787', 'C00221439', 'C00223414', 'C00225587', 'C00227922', 'C00227925', 'C00229317', 'C00229320', 'C00230508', 'C00233395', 'C00233812', 'C00233813', 'C00233816', 'C00233817', 'C00233818', 'C00233819', 'C00233820', 'C00234019', 'C00234297', 'C00234298', 'C00235439', 'C00235440', 'C00235633', 'C00237247-4100', 'C00237248-4100', 'C00238180-4100', 'C00238181-4100', 'C00241079-4100', 'C00243350', 'C00243765-4100', 'C00246076', 'C00246976', 'C00247596', 'C00248518-4100', 'C00249128-4100', 'C00250109', 'C00250110', 'C00250599-4100', 'C00254200-4100', 'C00254201-4100', 'C00254995-2150', 'C00257470', 'C00259011', 'C00259012', 'C00259013', 'C00259014', 'C00265847', 'C00265877-4100', 'C00267472', 'C00267523', 'C00270572', 'C00273483-4100', 'C00273753', 'C00274378', 'C00279853', 'C00283250-4100', 'C00284311', 'C00284405', 'C00285081', 'C00286159-4100', 'C00286759', 'C00287966', 'C00287967', 'C00289080-4100', 'C00290803-4100', 'C00290804-4100', 'C00294677-4100', 'C00294794-4100', 'C00299541', 'C00303771', 'C00303779', 'C00304649', 'C00304697-4100', 'C00304698-4100', 'C00306700-4100', 'C00307229', 'C00308207-4100', 'C00308691-4100', 'C00308789', 'C00311674-4100', 'C00319434', 'C00320144-4100', 'C00320145-4100', 'C00320146-4100', 'C00320147-4100', 'C00320158-4100', 'C00320159-4100', 'C00320251-4100', 'C00320252-4100', 'C00320640', 'C00322601', 'C00323925-4100', 'C00325156', 'C00331800', 'C00334164', 'C00334165', 'C00334166', 'C00334167', 'C00349765-A136', 'C00349766-A136', 'C00368321', 'C00403674', 'C00406026', 'C00423609', 'C00446282', 'C00453377', 'C00469711', 'C00471078', 'C00471087', 'C00472602', 'C00473445', 'C00521629', 'C00532115', 'C00539863', 'C00539866', 'C00539867', 'C00543551-bla', 'C00543551-blu', 'C00543551-gre', 'C00559196', 'C00559199', 'C00559202', 'C00559204', 'C00559206', 'C00563731', 'C00570061', 'C00570065', 'C00585980', 'C00587973', 'C00618313', 'C00618314', 'C00637484', 'C00638735', 'C00638736', 'C00642739', 'C00671897', 'C00678889', 'C00679772', 'C00690364', 'C00693370', 'C00697790', 'C00704930', 'C00704931', 'C00704932', 'C00729579', 'C00752821', 'C00888852']

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
