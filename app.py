import streamlit as st
import numpy as np
import pandas as pd
from constants import *
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics
# Todo
# 1. Y/N
# 2. L/S
# 3. Populate default value as 1st entry

# fw -> feed water
# ro -> RO water
# Dmin - >Dmineralized water
# Soft -> Soft water
# L S -> liquid / solid

st.title('Boiler Product Selector')
with st.form(key='my_form'):
    opco = st.selectbox('Country', ['USA','China','RSA','LATAM','Canada','EMEA'], index=0)
    psig1 = st.radio('Is pressure less than 10 bar ?', ('Yes','No'), index=0)
    psig2 = st.radio('Is pressure less than 60 bar ?', ('Yes','No'), index=0)
    # psig3 = st.radio('>870 PSIG (>60 BAR)', ('Yes','No'), index=0)

    sa = st.radio('Is it Single Active', ('Yes','No'), index=1)
    fw = st.selectbox('Feed water quality', ('Demineralized','RO'), index=1)
    internal = st.radio('Is it internal ?', ('Yes','No'), index=0)
    multipurpose = st.radio('Is it a multi purpose product ?', ('Yes','No'), index=0)
    sl_form = st.selectbox('Is it Solid/Liquid ?', ('Solid','Liquid'), index=0)
    co_ord = st.radio('Co-ord/ Congruent PO4', ('Yes','No'), index=1)
    po4 = st.selectbox('PO4', ('Yes','No'), index=0)
    cpo4 = st.radio('Chelant PO4', ('Yes','No'), index=1)
    all_poly = st.radio('All Poly', ('Yes','No'), index=1)
    na_po4 = st.selectbox('Does it have Na:PO4', ['Not applicable','Not recommended'], index=0)
    dairy = st.radio('Is it for dairy application ?', ('Yes','No'), index=1)
    food = st.radio('Is it for direct food application ?', ('Yes','No'), index=0)
    fda = st.selectbox('Select ffrom the list of FDA Approved direct contact limit',
                        ["Partially volatile", "Not Volatile", "No limit + Not Volatile", "< 33 ppm in steam, in NA it is 15 ppm", "NOT ALLOWED, in NA it is a limit of 10 ppm (total amine)", "<500 ppm in steam", "<70 ppm in steam", "<62 ppm in steam", "NOT ALLOWED", "No limit"],
                        index=0)
    defoamer = st.radio('Is it defoamer application ?', ('Yes','No'), index=1)
    avt = st.radio('Is there AVT ?', ('Yes','No'), index=1)
    n_amine = st.radio('Is there N Amine ?', ('Yes','No'), index=0)
    v_n_amine = st.radio('Is there volatile Ox scav & N amine ?', ('Yes','No'), index=1)
    steam = st.radio('Is there Steam & Condensate ?', ('Yes','No'), index=0)
    turbine = st.selectbox('Turbine used in Plant ?', ['Compatible, not beneficial, true but would never be used in a plant with a turbine', 'Yes', 'Compatible, not beneficial'], index=0)
    yellow = st.selectbox('Compatibility with Yellow metals', ['Yes', 'Compatible, not beneficial', 'No'], index=0)
    dr = st.selectbox('DR',["Not applicable", "Not recommended", '1.7', '1.84', '2.88', '1.3', '4.2'], index=0)
    f_amine = st.radio('Filming Amine', ('Yes','No'), index=1)
    tot_amine = st.selectbox('Total % Amine',['4.8', '0.0', '45.0', '42.0', '0.9', '35.0', '40.0', '30.0'], index=0)
    ox_scav = st.radio('Are there Ox scavengers ?', ('Yes','No'), index=0)
    contains_cat = st.radio('Is there catalyst ?', ('Yes','No'), index=1)
    passivation = st.radio('Is there Passivation ?', ('Yes','No'), index=1)
    submit_button = st.form_submit_button(label='Submit')
if submit_button:
    dset = pd.read_csv('all_data_encoded.csv')
    X = dset.drop(columns=['A9'])
    y = dset.A9
    X_train = X
    y_train = y
    clf = tree.DecisionTreeClassifier(max_depth=100)
    clf.fit(X_train,y_train)
    valv = list()
    opco_val = opco_dict[opco]
    for val in opco_val:
        valv.append(val)
    valv.extend(
        [psig1_dict[psig1],
        psig2_dict[psig2],
        sa_dict[sa],
        fw_dict[fw],
        internal_dict[internal],
        multipurpose_dict[multipurpose],
        sl_form_dict[sl_form],
        co_ord_dict[co_ord],
        po4_dict[po4],
        cpo4_dict[cpo4],
        all_poly_dict[all_poly],
        na_po4_dict[na_po4],
        dairy_dict[dairy],
        food_dict[food],
        fda_dict[fda],
        defoamer_dict[defoamer],
        avt_dict[avt],
        n_amine_dict[n_amine],
        v_n_amine_dict[v_n_amine],
        steam_dict[steam],
        turbine_dict[turbine],
        yellow_dict[yellow],
        dr_dict[dr],
        f_amine_dict[f_amine],
        tot_amine_dict[tot_amine],
        ox_scav_dict[ox_scav],
        contains_cat_dict[contains_cat],
        passivation_dict[passivation] 
        ]
    )
    
    # print('=================')
    # print(X.values.tolist()[0])
    # print(valv)
    m = [valv==i for i in X.values.tolist()]
    print(m)
    if any(m):
        valv_df = pd.DataFrame(valv).transpose()
        valv_df.columns = X.columns
        pred_ui = clf.predict(valv_df)
        print(pred_ui)
        st.success(f'The product for the following configuration is {pred_ui}')
    else:
        print('Not here')
        st.error('''
        We could not find a product for such an input combination :( 
        Please re-check the i/p condition or parameters!
        ''')
    
 



