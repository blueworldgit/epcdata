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
codes = ['B00003507', 'B00003508', 'B00003509', 'B00003510', 'B00003511', 'B00003512', 'B00004034', 'B00004035', 'B00004040', 'B00004085', 'B00004087', 'B00004088', 'B00004090', 'B00004108', 'B00004142', 'B00004151', 'B00004153', 'B00004199', 'B00004274', 'B00004303', 'B00004623', 'B00004653', 'B00004679', 'B00004681', 'B00004683', 'B00004729', 'B00004762', 'B00004794', 'B00004796', 'B00004799', 'B00004839', 'B00004848', 'B00004849', 'B00004851', 'B00004856', 'B00004859', 'B00004861', 'B00004865', 'B00004906', 'B00004940', 'B00004941', 'B00004953', 'B00004955', 'B00004956', 'B00004957', 'B00004966', 'B00004983', 'B00004988', 'B00005177', 'B00005180', 'B00005209', 'B00005251', 'B00005252', 'B00005253', 'B00005254', 'B00005301', 'B00005308', 'B00005316', 'B00005330', 'B00005351', 'B00005363', 'B00005370', 'B00005376', 'B00005404', 'B00005409', 'B00005410', 'B00005419', 'B00005444', 'B00005477', 'B00005714', 'B00005799', 'B00005805', 'B00006002', 'B00006003', 'B00006005', 'B00006008', 'B00006009', 'B00006012', 'B00006013', 'B00006014', 'B00006019', 'B00006020', 'B00006022', 'B00006023', 'B00006026', 'B00006028', 'B00006031', 'B00006032', 'B00006034', 'B00006041', 'B00006042', 'B00006043', 'B00006046', 'B00006047', 'B00006050', 'B00006116', 'B90000033', 'B90000035', 'B90000149', 'B90000621', 'B90000627', 'B90000639', 'B90000877', 'B90001103', 'B90001169', 'B90001171', 'B90001194', 'B90001293', 'B90001294', 'B90001298', 'C00001339', 'C00002908', 'C00002920', 'C00003209', 'C00003686', 'C00003695', 'C00003696', 'C00004150', 'C00004535', 'C00013590', 'C00014021', 'C00017370', 'C00017616', 'C00017617', 'C00017618', 'C00017619', 'C00017620', 'C00017621', 'C00017622', 'C00017623', 'C00017624', 'C00017625', 'C00017626', 'C00017627', 'C00017865', 'C00018966', 'C00022380', 'C00024572', 'C00024573', 'C00024970', 'C00029566', 'C00030048', 'C00031533', 'C00032363', 'C00033625', 'C00037326', 'C00040010', 'C00041192', 'C00041988', 'C00042951', 'C00047244', 'C00047796', 'C00049994', 'C00050126', 'C00050133', 'C00050142', 'C00050143', 'C00050168', 'C00050531', 'C00050803', 'C00053801', 'C00053812', 'C00054400', 'C00054625', 'C00055163', 'C00055184', 'C00056376', 'C00056542', 'C00059723', 'C00059724', 'C00059724-A148', 'C00065153', 'C00066076', 'C00066128', 'C00066129', 'C00067424', 'C00069105', 'C00071769', 'C00071771', 'C00071910', 'C00071915', 'C00071918', 'C00072180', 'C00072270-B', 'C00072270-C', 'C00072270-D', 'C00072270-E', 'C00072270-F', 'C00072270-G', 'C00072272', 'C00072843', 'C00072894', 'C00072951', 'C00072983', 'C00073005', 'C00073006', 'C00073007', 'C00073038', 'C00073043-bla', 'C00073043-blu', 'C00073043-gre', 'C00073044-bla', 'C00073044-blu', 'C00073044-gre', 'C00073045-bla', 'C00073045-blu', 'C00073045-gre', 'C00073046-bla', 'C00073046-blu', 'C00073046-gre', 'C00073048', 'C00073528', 'C00073692', 'C00073808', 'C00074009', 'C00074267', 'C00074268', 'C00074269', 'C00074401', 'C00074545', 'C00074546', 'C00074696', 'C00074697', 'C00074698', 'C00074745', 'C00074815', 'C00074816', 'C00074848', 'C00075208', 'C00075224', 'C00075227', 'C00075228', 'C00075246', 'C00075250', 'C00075255', 'C00075258', 'C00075264', 'C00075266', 'C00075267', 'C00075268', 'C00075276', 'C00075282', 'C00075314', 'C00075416', 'C00075417', 'C00075418', 'C00075448', 'C00075566', 'C00075677', 'C00075679', 'C00075681', 'C00075800', 'C00076113', 'C00076114', 'C00076245', 'C00076388', 'C00076423', 'C00076424', 'C00076501', 'C00076502', 'C00076503', 'C00077076', 'C00077261', 'C00077262', 'C00077409', 'C00077423', 'C00077424', 'C00077425', 'C00077426', 'C00077427', 'C00077428', 'C00077430', 'C00077431', 'C00078100', 'C00078118', 'C00078151', 'C00078295', 'C00078317', 'C00078722', 'C00078725', 'C00079022', 'C00079023', 'C00079024', 'C00079034', 'C00079036', 'C00079037', 'C00079038', 'C00079141', 'C00079142', 'C00079178', 'C00079184', 'C00079457', 'C00079649', 'C00079751', 'C00080001', 'C00080006', 'C00080009', 'C00080545', 'C00080566', 'C00080583', 'C00080744', 'C00080774', 'C00081098', 'C00081099', 'C00082115', 'C00082170', 'C00082240', 'C00083228', 'C00084054', 'C00084089', 'C00084095', 'C00084100', 'C00084108', 'C00084212', 'C00084385', 'C00084404', 'C00084409', 'C00084813', 'C00084848', 'C00084952', 'C00085281', 'C00085289', 'C00085305', 'C00085306', 'C00085307', 'C00085308', 'C00085309', 'C00085311', 'C00085630', 'C00085986', 'C00085988', 'C00086304', 'C00086306', 'C00086307', 'C00086309', 'C00086768', 'C00086848', 'C00086849', 'C00087383', 'C00087451', 'C00087683', 'C00087852', 'C00088004', 'C00088108', 'C00088203', 'C00088252', 'C00088254', 'C00088303', 'C00088305', 'C00088307', 'C00088309', 'C00088435', 'C00088574', 'C00088809', 'C00088979', 'C00089072', 'C00089075', 'C00089306', 'C00089373', 'C00089625', 'C00089667', 'C00089670', 'C00089671', 'C00089672', 'C00089673', 'C00090243', 'C00090363', 'C00090367', 'C00090601', 'C00090602', 'C00090639', 'C00090657', 'C00091580', 'C00091603', 'C00091604', 'C00091605', 'C00091606', 'C00092299', 'C00092653', 'C00093416', 'C00093421', 'C00093567', 'C00093568', 'C00093573', 'C00093574', 'C00093576', 'C00093579', 'C00093580', 'C00093586', 'C00093590', 'C00093592', 'C00093596', 'C00093597', 'C00093603', 'C00093605', 'C00093606', 'C00093611', 'C00093613', 'C00093614', 'C00093615', 'C00093621', 'C00093626', 'C00093627', 'C00093632', 'C00093639', 'C00093640', 'C00093645', 'C00093649', 'C00093656', 'C00093657', 'C00093661', 'C00093672', 'C00093673', 'C00093679', 'C00093880', 'C00093882', 'C00095484', 'C00096310', 'C00096937', 'C00097689', 'C00097934', 'C00099220', 'C00100170', 'C00100304', 'C00100328', 'C00101117', 'C00101688', 'C00101692', 'C00101837', 'C00102252', 'C00103109', 'C00103111', 'C00103977', 'C00104607', 'C00104774', 'C00105159', 'C00106163', 'C00107565', 'C00107793', 'C00108602', 'C00108605', 'C00108625', 'C00109635', 'C00110036', 'C00110052', 'C00111120', 'C00111121', 'C00112090', 'C00112093', 'C00112425', 'C00112684', 'C00112886', 'C00112937', 'C00112939', 'C00112940', 'C00112941', 'C00113071', 'C00113072', 'C00113073', 'C00113074', 'C00113075', 'C00117641', 'C00118506', 'C00118992', 'C00119168', 'C00120455', 'C00120499', 'C00120500', 'C00120683', 'C00121212', 'C00121213', 'C00121214', 'C00121215', 'C00121217', 'C00121218', 'C00121220', 'C00121224', 'C00122508', 'C00122656', 'C00123710', 'C00124885', 'C00124984', 'C00125940', 'C00127834', 'C00128220', 'C00128466', 'C00128467', 'C00128471', 'C00128477', 'C00128480', 'C00128483', 'C00128485', 'C00128486', 'C00128487', 'C00128489', 'C00128902', 'C00129581', 'C00130628', 'C00131184', 'C00134346', 'C00134933', 'C00137513', 'C00138891', 'C00140197', 'C00140220', 'C00141860', 'C00142756', 'C00145293', 'C00146565', 'C00149328', 'C00149660', 'C00154341', 'C00155247', 'C00155266', 'C00155407', 'C00155802', 'C00156174', 'C00156354', 'C00156372', 'C00156373', 'C00156374', 'C00156375', 'C00156376', 'C00156377', 'C00157035', 'C00157176', 'C00158182', 'C00159353', 'C00161351', 'C00161354', 'C00161521', 'C00161522', 'C00162402', 'C00165508', 'C00165627', 'C00165870', 'C00166321', 'C00166469', 'C00168730', 'C00168783', 'C00168789', 'C00170058', 'C00175205', 'C00175451', 'C00176660', 'C00176661', 'C00176662', 'C00178142', 'C00178146', 'C00178713', 'C00178788', 'C00178790', 'C00178793', 'C00178794', 'C00178797', 'C00178798', 'C00178840', 'C00180031', 'C00180032', 'C00180163', 'C00180581', 'C00180583', 'C00180586', 'C00180598', 'C00180602', 'C00180866', 'C00181036', 'C00181037', 'C00182187', 'C00184187', 'C00184188', 'C00184428', 'C00184433', 'C00184468', 'C00184779', 'C00184780', 'C00184782', 'C00184831', 'C00185436', 'C00185481', 'C00185533', 'C00185536', 'C00185538', 'C00185546', 'C00185553', 'C00185555', 'C00185559', 'C00185581', 'C00185593', 'C00185594', 'C00185602', 'C00185605', 'C00185606', 'C00185628', 'C00185630', 'C00185631', 'C00185652', 'C00185653', 'C00185654', 'C00185655', 'C00185657', 'C00185735', 'C00185847', 'C00186582', 'C00186591', 'C00186732', 'C00187143', 'C00187946', 'C00188538', 'C00190097', 'C00190098', 'C00190099', 'C00190118', 'C00190121', 'C00191058', 'C00191100-F139', 'C00191101-F139', 'C00191105', 'C00193350', 'C00193531', 'C00193841', 'C00194267', 'C00194268', 'C00196977', 'C00197288', 'C00197291', 'C00197475', 'C00197479', 'C00197486', 'C00198887', 'C00198891', 'C00199382', 'C00199629', 'C00199630', 'C00200001', 'C00200425', 'C00200878', 'C00201270', 'C00202003', 'C00203497', 'C00203500', 'C00203960', 'C00204039', 'C00204040', 'C00204309', 'C00204439', 'C00205079', 'C00205306', 'C00205331', 'C00206218', 'C00206219', 'C00207615', 'C00207820', 'C00210637', 'C00210671', 'C00210675', 'C00210732', 'C00210733', 'C00211077', 'C00211082', 'C00211099', 'C00211100', 'C00211122', 'C00211163', 'C00211164', 'C00211165', 'C00211169', 'C00211244', 'C00211245', 'C00211246', 'C00211248', 'C00211379', 'C00213323', 'C00213490-A', 'C00213490-B', 'C00213490-C', 'C00213563', 'C00213564', 'C00213565', 'C00213568', 'C00213571', 'C00213573', 'C00213574', 'C00213575', 'C00213576', 'C00213577', 'C00213578', 'C00213579', 'C00213581', 'C00213582', 'C00213583', 'C00213625', 'C00215105', 'C00215224', 'C00215289', 'C00215481', 'C00216475', 'C00217151', 'C00217155', 'C00217158', 'C00217160', 'C00217168', 'C00217169', 'C00217173', 'C00217174', 'C00217175', 'C00217176', 'C00217179', 'C00217181', 'C00217182', 'C00217183', 'C00217185', 'C00217188', 'C00217189', 'C00217197', 'C00217198', 'C00217199', 'C00217200', 'C00217202', 'C00217207', 'C00217208', 'C00217209', 'C00217211', 'C00217212', 'C00217214', 'C00217234', 'C00217241', 'C00217382', 'C00217384', 'C00217701', 'C00217885', 'C00217905', 'C00217934', 'C00217938', 'C00217943', 'C00217948', 'C00217959', 'C00218066', 'C00218086', 'C00218120', 'C00218225', 'C00218295', 'C00218298', 'C00218303', 'C00218479', 'C00218906', 'C00218907', 'C00218911', 'C00221029', 'C00222037', 'C00222194', 'C00222329', 'C00224309', 'C00224311', 'C00224808', 'C00225537', 'C00226796', 'C00227566', 'C00227567', 'C00227697', 'C00228725', 'C00228727', 'C00228730', 'C00228749', 'C00228863', 'C00228880', 'C00229296', 'C00229774', 'C00229775', 'C00229941', 'C00229942', 'C00229943', 'C00229965', 'C00230235', 'C00230243', 'C00230271', 'C00230356', 'C00230882', 'C00230885', 'C00231992', 'C00232257', 'C00232570', 'C00233435', 'C00233501', 'C00235628', 'C00237202', 'C00237593', 'C00237904', 'C00238238', 'C00238588', 'C00238589', 'C00238591', 'C00238592', 'C00238594', 'C00238599', 'C00238600', 'C00238609', 'C00238670', 'C00238674', 'C00238676', 'C00238678', 'C00238681', 'C00238683', 'C00238687', 'C00238689', 'C00238707', 'C00238756', 'C00238763', 'C00238764', 'C00238769', 'C00238771', 'C00238773', 'C00238774', 'C00238776', 'C00238777', 'C00238779', 'C00238782', 'C00241034', 'C00245347', 'C00247985', 'C00248042', 'C00248050', 'C00248054', 'C00248056', 'C00248057', 'C00248838', 'C00248843', 'C00250170', 'C00250171', 'C00250715', 'C00253426', 'C00253427', 'C00253428', 'C00253430', 'C00253479', 'C00254437', 'C00258299', 'C00260664', 'C00264290', 'C00265292', 'C00265293', 'C00266855', 'C00268265', 'C00268268', 'C00268859', 'C00271216-B', 'C00271216-C', 'C00271216-D', 'C00271216-E', 'C00271216-F', 'C00271216-G', 'C00271290', 'C00274667', 'C00275602', 'C00275603', 'C00276004', 'C00280656', 'C00283275', 'C00283466', 'C00283478', 'C00283549', 'C00283684', 'C00287486', 'C00289324', 'C00290871', 'C00291102', 'C00293736', 'C00296126', 'C00300179', 'C00300495', 'C00306666', 'C00308737', 'C00308847', 'C00310877', 'C00311990', 'C00320324', 'C00322226', 'C00324241', 'C00325156', 'C00325450', 'C00333494', 'C00333495', 'C00333890', 'C00333977', 'C00334116', 'C00334135', 'C00337351', 'C00341433', 'C00342451', 'C00344866', 'C00345124', 'C00345777', 'C00347792', 'C00348029', 'C00349003', 'C00349004', 'C00383515', 'C00384459', 'C00389561', 'C00389563', 'C00397473', 'C00403384-A', 'C00403384-B', 'C00403384-C', 'C00403702', 'C00413044', 'C00419031', 'C00419032', 'C00421273', 'C00421559', 'C00423186', 'C00423608', 'C00423609', 'C00427675', 'C00427755', 'C00429557', 'C00430210', 'C00440659', 'C00444868', 'C00446282', 'C00446283', 'C00451027', 'C00452602', 'C00452603', 'C00457818', 'C00457823', 'C00469711', 'C00472104', 'C00472105', 'C00472602', 'C00472950', 'C00473445', 'C00473655', 'C00473658', 'C00473659', 'C00489665', 'C00489676', 'C00489677', 'C00492869', 'C00494020', 'C00514960', 'C00518592', 'C00521629', 'C00525877', 'C00530682', 'C00532115', 'C00542187', 'C00542612', 'C00542614', 'C00543551-bla', 'C00543551-blu', 'C00543551-gre', 'C00559196', 'C00559199', 'C00559202', 'C00559204', 'C00559206', 'C00563460', 'C00563731', 'C00564029', 'C00564034', 'C00564036', 'C00564037', 'C00564038', 'C00564039', 'C00564040', 'C00564041', 'C00564043', 'C00564044', 'C00566514', 'C00566873', 'C00566949', 'C00568894', 'C00570061', 'C00570062', 'C00570063', 'C00570064', 'C00570065', 'C00577454', 'C00577808', 'C00581010', 'C00585980', 'C00587973', 'C00608918', 'C00614492', 'C00627851', 'C00637484', 'C00638474', 'C00638478', 'C00638479', 'C00638735', 'C00638736', 'C00642739', 'C00649758', 'C00653806', 'C00671897', 'C00697790', 'C00704930', 'C00704931', 'C00704932', 'C00729579', 'C00888852', 'C00888880', 'C00888881', 'C00888882']

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
