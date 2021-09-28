import streamlit as st
import numpy as np
import pandas as pd
from constants import *
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics
submit_button=None

def internal_function():
    st.markdown("## Internal Treatment")
    internal = st.radio('Is an Internal Treatment product only required ?', ('Yes','No'), index=0)
    po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ('Yes','No'), index=0)
    return (internal, po4)

def amine_function():
    st.markdown("## Neutralizing amine")
    n_amine = st.radio('Is Neutralizing Amine treatment required for steam and condensate treatment?', ('Yes','No'), index=0)
    yellow = st.radio('Is it compatible with Yellow metals ?', ['Yes', 'No'], index=0)
    dr = st.selectbox('Distribution ratio', ['< 2.4', '> 2.4','Not Applicable'], index=0)
    return (n_amine, yellow, dr)

def defoamer_function():
    st.markdown("## Defoamer")
    defoamer = st.radio('Is a Defoamer required ?', ('Yes','No'), index=1)
    return defoamer

def ox_scav_function():
    st.markdown("## Oxygen Scavengers")
    ox_scav = st.radio('Is Oxygen Scavenger required ?', ('Yes','No'), index=0)
    passivation = st.radio('Is it a Passivation product ?', ('Yes','No'), index=1)
    contains_cat = st.radio('Is there catalyst in the product ?', ('Yes','No'), index=1)
    return (ox_scav, passivation, contains_cat)

st.title('Boiler Product Selector')

opco = st.selectbox('Operating Country (OPCO)', ['USA','China','RSA','LATAM','Canada','EMEA'], index=0)
op_pres = st.selectbox('Operating Pressure', ('Less than 60 Bar','Between 10 to 60 Bar'), index=0)
fw = st.selectbox('Feed water quality (RO / Demineralized)', ('All (Raw, RO, Demin)','Raw, RO only'), index=0)
fda = st.radio('Is it FDA approved for direct food application?',('Yes','No'))
dairy = st.radio('Is it for Dairy application ?', ('Yes','No'), index=0)
func_type = st.selectbox('Type of function required',(
    '---------',
    'Multi Functional (Internal + Amine + O2)',
    'Multi Functional (Amine + O2)',
    'Multi Functional (Internal + Defoamer)',
    'Single Functional Products'
),index=0)


if func_type=='Multi Functional (Internal + Amine + O2)':
    sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0)
    
    defoamer = 'No'
    internal,po4 = internal_function()
    n_amine, yellow, dr = amine_function()
    ox_scav, passivation, contains_cat = ox_scav_function()
    opco_val = opco_dict[opco]
    valv = list()
    valv = valv + opco_val
    
    valv.extend(
        [
        op_pres_dict[op_pres],
        fw_dict[fw],
        fda_dict[fda],
        dairy_dict[dairy],
        func_type_dict[func_type],
        sl_dict[sl],
        internal_dict[internal],
        po4_dict[po4],
        defoamer_dict[defoamer],
        n_amine_dict[n_amine],
        yellow_dict[yellow],
        dr_dict[dr],
        ox_scav_dict[ox_scav],
        passivation_dict[passivation],
        contains_cat_dict[contains_cat],
        ]
    )
    submit_button = st.button(label='Submit')

if func_type=='Multi Functional (Amine + O2)':
    sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0)

    internal = 'No'
    po4 = 'No'
    defoamer = 'No'
    n_amine, yellow, dr = amine_function()
    ox_scav, passivation, contains_cat = ox_scav_function()
    opco_val = opco_dict[opco]
    valv = list()
    valv = valv + opco_val
    defoamer = 'No'
    valv.extend(
        [
        op_pres_dict[op_pres],
        fw_dict[fw],
        fda_dict[fda],
        dairy_dict[dairy],
        func_type_dict[func_type],
        sl_dict[sl],
        internal_dict[internal],
        po4_dict[po4],
        defoamer_dict[defoamer],
        n_amine_dict[n_amine],
        yellow_dict[yellow],
        dr_dict[dr],
        ox_scav_dict[ox_scav],
        passivation_dict[passivation],
        contains_cat_dict[contains_cat],
        ]
    )
    submit_button = st.button(label='Submit')

        
if func_type=='Multi Functional (Internal + Defoamer)':
    sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0)

    n_amine = 'No'
    yellow = "No"
    dr = "Not Applicable"
    ox_scav = 'No'
    passivation = 'No'
    contains_cat = 'No'
    internal,po4 = internal_function()
    defoamer = defoamer_function()
    opco_val = opco_dict[opco]
    valv = list()
    valv = valv + opco_val
    valv.extend(
        [
        op_pres_dict[op_pres],
        fw_dict[fw],
        fda_dict[fda],
        dairy_dict[dairy],
        func_type_dict[func_type],
        sl_dict[sl],
        internal_dict[internal],
        po4_dict[po4],
        defoamer_dict[defoamer],
        n_amine_dict[n_amine],
        yellow_dict[yellow],
        dr_dict[dr],
        ox_scav_dict[ox_scav],
        passivation_dict[passivation],
        contains_cat_dict[contains_cat],
        ]
    )
    submit_button = st.button(label='Submit')
if func_type=='Single Functional Products':
    master_list = {
        'valv1': None,
        'valv2': None,
        'valv3':None,
        'valv4':None
    }
    # Internal
    st.markdown("## Internal Treatment")
    internal = st.radio('Is an Internal Treatment product only required ?', ('Yes','No'), index=1)
    # po4 = 'No'
    if internal == 'Yes':
        sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0, key='1')
        po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ('Yes','No'), index=0)
        opco_val = opco_dict[opco]
        valv1 = list()
        valv1 = valv1 + opco_val
        valv1.extend(
            [
            op_pres_dict[op_pres],
            fw_dict[fw],
            fda_dict[fda],
            dairy_dict[dairy],
            func_type_dict[func_type],
            sl_dict[sl],
            internal_dict[internal],
            po4_dict[po4],
            defoamer_dict['No'],
            n_amine_dict['No'],
            yellow_dict['No'],
            dr_dict['Not Applicable'],
            ox_scav_dict['No'],
            passivation_dict['No'],
            contains_cat_dict['No'],
            ]
        )
        master_list['valv1'] = valv1
    # st.write(master_list)
    # amine
    st.markdown("## Neutralizing amine")
    n_amine = st.radio('Is Neutralizing Amine treatment required for steam and condensate treatment?', ('Yes','No'), index=1)
    # yellow='No'
    # dr = 'Not Applicable'
    if n_amine == 'Yes':
        sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0, key='2')
        yellow = st.radio('Is it compatible with Yellow metals ?', ['Yes', 'No'], index=0)
        dr = st.selectbox('Distribution ratio', ['< 2.4', '> 2.4','Not Applicable'], index=0)
        opco_val = opco_dict[opco]
        valv2 = list()
        valv2 = valv2 + opco_val
        valv2.extend(
            [
            op_pres_dict[op_pres],
            fw_dict[fw],
            fda_dict[fda],
            dairy_dict[dairy],
            func_type_dict[func_type],
            sl_dict[sl],
            internal_dict['No'],
            po4_dict['No'],
            defoamer_dict['No'],
            n_amine_dict[n_amine],
            yellow_dict[yellow],
            dr_dict[dr],
            ox_scav_dict['No'],
            passivation_dict['No'],
            contains_cat_dict['No'],
            ]
        )
        master_list['valv2'] = valv2
    # st.write(master_list)
    # Defoamer
    st.markdown("## Defoamer")
    defoamer = st.radio('Is a Defoamer required ?', ('Yes','No'), index=1)
    if defoamer == 'Yes':
        sl = st.radio('Is a Solid/Liquid product required?', ['Liquid'], key='3')
        opco_val = opco_dict[opco]
        valv3 = list()
        valv3 = valv3 + opco_val
        valv3.extend(
            [
            op_pres_dict[op_pres],
            fw_dict[fw],
            fda_dict[fda],
            dairy_dict[dairy],
            func_type_dict[func_type],
            sl_dict[sl],
            internal_dict['No'],
            po4_dict['No'],
            defoamer_dict[defoamer],
            n_amine_dict['No'],
            yellow_dict['No'],
            dr_dict['Not Applicable'],
            ox_scav_dict['No'],
            passivation_dict['No'],
            contains_cat_dict['No'],
            ]
        )
        master_list['valv3'] = valv3
    # st.write(master_list)
    # OX scav 
    st.markdown("## Oxygen Scavengers")
    ox_scav = st.radio('Is Oxygen Scavenger required ?', ('Yes','No'), index=1)
    passivation='No'
    contains_cat = 'No'
    if ox_scav=='Yes':
        sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0,key='4')
        passivation = st.radio('Is it a Passivation product ?', ('Yes','No'), index=1)
        contains_cat = st.radio('Is there catalyst in the product ?', ('Yes','No'), index=1)
        opco_val = opco_dict[opco]
        valv4 = list()
        valv4 = valv4 + opco_val
        valv4.extend(
            [
            op_pres_dict[op_pres],
            fw_dict[fw],
            fda_dict[fda],
            dairy_dict[dairy],
            func_type_dict[func_type],
            sl_dict[sl],
            internal_dict['No'],
            po4_dict['No'],
            defoamer_dict['No'],
            n_amine_dict['No'],
            yellow_dict['No'],
            dr_dict['Not Applicable'],
            ox_scav_dict[ox_scav],
            passivation_dict[passivation],
            contains_cat_dict[contains_cat],
            ]
        )
        master_list['valv4'] = valv4
    # st.write(master_list)
    submit_button = st.button(label='Submit')

if submit_button:
    dset = pd.read_csv('Test_v4refine.csv')
    X = dset.drop(columns=['V'])
    y = dset['V']
    X_train = X
    y_train = y
    clf = tree.DecisionTreeClassifier(max_depth=100)
    clf.fit(X_train,y_train)
    if func_type !='Single Functional Products':
        m = [valv==i for i in X.values.tolist()]
        print(m)
#         st.write(valv)
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
        # st.write(valv)
    else:
        # st.write(master_list)
        final_prods = list()
        for key,val in master_list.items():
            valv = master_list[key]
            if valv != None:
                # st.write(f'checking {key}')
                m = [valv==i for i in X.values.tolist()]
                if any(m):
                    valv_df = pd.DataFrame(valv).transpose()
                    valv_df.columns = X.columns
                    pred_ui = clf.predict(valv_df)
                    final_prods.extend(pred_ui)
                    # st.write(f'found {key}')
                
        if len(final_prods) < 1:
            st.error('''
            We could not find a product for such an input combination :( 
            Please re-check the input condition or parameters!
            ''')
        else:
            final_prods_res = ', '.join(final_prods)
            st.success(f'The product(s) for the above configuration is/are {final_prods_res}')


    

   
