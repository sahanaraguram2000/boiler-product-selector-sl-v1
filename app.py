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
    opco = st.selectbox('Operating Country (OPCO)', ['USA','China','RSA','LATAM','Canada','EMEA'], index=0)
    psig1 = st.radio('Is pressure less than 10 bar ?', ('Yes','No'), index=0)
    psig2 = st.radio('Is pressure less than 60 bar ?', ('Yes','No'), index=0)
    sa = st.radio('Is it Single Active ?', ('Yes','No'), index=1)
    fw = st.selectbox('Feed water quality (RO / Demineralized)', ('Demineralized','RO'), index=0)
    sl_form = st.selectbox('Is it Solid/Liquid product ?', ('Solid','Liquid'), index=0)
    dairy = st.radio('Is it for Dairy application ?', ('Yes','No'), index=1)
    food = st.radio('Is it for direct food application ?', ('Yes','No'), index=0)
    fda = st.selectbox('Is it FDA approved for direct contact ? [Yes(Refer to US FDA for details or contact SME)/No]' ,
                    ["Yes (refer to US FDA for details or contact SME)", "No"],
                    index=0)
    avt = st.radio('Is All Volatile Treatment (AVT) required ? (Only for Neutralizing Amine or Oxygen Scavenger)', ('Yes','No'), index=1)
    

    st.markdown("## Internal Treatment")
    internal = st.radio('Is an Internal Treatment product only required ?', ('Yes','No'), index=0)
    multipurpose = st.radio('Is a Multipurpose product (Internal + Steam & Condensate) required ?', ('Yes','No'), index=0)
    po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ('Yes','No'), index=0)

    defoamer = st.radio('Is a Defoamer required ?', ('Yes','No'), index=1)

    st.markdown("## Condensate Treatment (Neutralizing Amine) ")

    n_amine = st.radio('Is Neutralizing Amine treatment required ?', ('Yes','No'), index=0)
    v_n_amine = st.radio('Is a volatile Oxygen Scavenger and Neutralizing Amine required in the same product ?', ('Yes','No'), index=1)
    steam = st.radio('Is treatment of Steam & Condensate required?', ('Yes','No'), index=0)
    yellow = st.selectbox('Is it compatible with Yellow metals ?', ['Yes', 'No'], index=0)
    dr = st.selectbox('Distribution Ratio of Amines',["Not applicable", '< 2.4', '> 2.4'], index=0)


    st.markdown("## Oxygen Scavenger Treatment")

    ox_scav = st.radio('Are there Ox scavengers ?', ('Yes','No'), index=0)
    passivation = st.radio('Is there Passivation ?', ('Yes','No'), index=1)
    contains_cat = st.radio('Is there catalyst in the product ?', ('Yes','No'), index=1)
    submit_button = st.form_submit_button(label='Submit')
if submit_button:
    dset = pd.read_csv('Test_v2refine.csv')
    X = dset.drop(columns=['A2'])
    y = dset.A2
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
        # co_ord_dict[co_ord],
        po4_dict[po4],
        # cpo4_dict[cpo4],
        # all_poly_dict[all_poly],
        # na_po4_dict[na_po4],
        dairy_dict[dairy],
        food_dict[food],
        fda_dict[fda],
        defoamer_dict[defoamer],
        avt_dict[avt],
        n_amine_dict[n_amine],
        v_n_amine_dict[v_n_amine],
        steam_dict[steam],
        # turbine_dict[turbine],
        yellow_dict[yellow],
        dr_dict[dr],
        # f_amine_dict[f_amine],
        # tot_amine_dict[tot_amine],
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
