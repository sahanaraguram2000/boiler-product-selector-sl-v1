import streamlit as st
import numpy as np
import pandas as pd
from constants import *
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics


dset = pd.read_csv('Test_v4refine.csv')

def internal_function():
    st.markdown("## Internal Treatment")
    # internal = st.radio('Is an Internal Treatment product only required ?', ('Yes','No'), index=0)
    internal = 'Yes'
    po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ('Yes','No'), index=0)
    return (internal, po4)

def amine_function():
    st.markdown("## Neutralizing amine")
    # n_amine = st.radio('Is Neutralizing Amine treatment required for steam and condensate treatment?', ('Yes','No'), index=0)
    n_amine = 'Yes'
    yellow = st.radio('Is there Yellow metal in the system?', ['Yes', 'No'], index=0)
    if yellow == 'No':
        dset['Q']=dset['Q'].replace({1:0})
    dr = st.selectbox('Distribution ratio', ['< 2.4', '> 2.4','Not Applicable'], index=0)
    return (n_amine, yellow, dr)

def defoamer_function():
    # st.markdown("## Defoamer")
    # defoamer = st.radio('Is a Defoamer required ?', ('Yes','No'), index=1)
    defoamer = 'Yes'
    return defoamer

def ox_scav_function():
    st.markdown("## Oxygen Scavengers")
    # ox_scav = st.radio('Is Oxygen Scavenger required ?', ('Yes','No'), index=0)
    ox_scav = 'Yes'
    passivation = st.radio('Is Passivation Required?', ('Yes','No'), index=1)
    contains_cat = st.radio('Is a product that contains catalyst required ?', ('Yes','No'), index=1)
    return (ox_scav, passivation, contains_cat)

def product_selector():
    submit_button=None
    opco = st.selectbox('Operating Country (OPCO)', ['USA','China','RSA','LATAM','Canada','EMEA'], index=0)
    opco_pres_1 = st.slider('Operating Pressure (bar)',min_value=0, max_value=60)
    if opco_pres_1 < 10:
        op_pres = 'Less than 60 Bar'
        # dset['G'] = dset['G'].replace({2:1})
    else:
        op_pres = 'Between 10 to 60 Bar'
        dset['G'] = dset['G'].replace({1:2})
    # op_pres_1 = st.radio('Is the pressure less than 60 bar and between 10 and 60?', ('Yes','No'), index=0)
    # if op_pres_1=='Yes':
    #     op_pres = 'Less than 10 Bar'
    # else:
    #     op_pres_2 = st.radio('Is the pressure less than 60 bar?', ('Yes','No'), index=0)
    #     if op_pres_2 == 'Yes':
    #         op_pres = 'Less than 10 Bar'
    #     else:
    #         st.warning('''
    #             The product selector is only for low pressure boilers less than 60 bars.
    #             ''')
    fw = st.selectbox('Feed Water Quality', ('All (Raw/RO/Demineralized)', 'Raw, RO Only'), index=0)
    if fw=='Raw, RO Only':
        dset['H'] = dset['H'].replace({1:2})
        # fw='All (Raw, RO, Demin)'
    # check1 = st.checkbox('Raw')
    # check2 = st.checkbox('RO')
    # check3 = st.checkbox('Demin')

    fda = st.radio('Is an FDA approved product for direct food application required? ',('Yes','No'))
    if fda == 'No':
        dset['I'] = dset['I'].replace({0:1})
        fda = 'Yes'
    dairy = st.radio('Is it for Dairy application ?', ('Yes','No'), index=0)
    if dairy == 'No':
        dset['J'] = dset['J'].replace({0:1})
        dairy = 'Yes'
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
        sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=1)

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
        internal = st.radio('Is Internal treatment required?', ('Yes','No'), index=1)
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
            yellow = st.radio('Is there Yellow metal in the system?', ['Yes', 'No'], index=0)
            if yellow == 'No':
                dset['Q']=dset['Q'].replace({1:0})
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
            # sl = st.radio('Is a Solid/Liquid product required?', ['Liquid'], key='3')
            sl = 'Liquid'
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
            passivation = st.radio('Is Passivation Required?', ('Yes','No'), index=1)
            contains_cat = st.radio('Is a product that contains catalyst required?', ('Yes','No'), index=1)
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
        X = dset.drop(columns=['V'])
        y = dset['V']
        X_train = X
        y_train = y
        clf = tree.DecisionTreeClassifier(max_depth=100)
        clf.fit(X_train,y_train)
        if func_type !='Single Functional Products':
            m = [valv==i for i in X.values.tolist()]
            print(m)
            st.write(valv)
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
                Please re-check the input condition or parameters!
                ''')
            # st.write(valv)
        else:
            # st.write(master_list)
            final_prods = list()
            final_prods_keys = [
                'Internal treatment',
                'Neutralizing amine',
                'Defoamer',
                'Oxygen Scavengers'

            ]
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
                    else:
                        final_prods.extend(['No product found'])
                        # st.write(f'found {key}')
                else:
                    final_prods.extend(['No product found'])

            final_zip = list(zip(final_prods,final_prods_keys))
            final_dict = {}
            for val,key in final_zip:
                final_dict[key] = [val]
            final_df = pd.DataFrame(final_dict).T
            final_df.columns = ['Products']
                

            if len(final_prods) < 1:
                st.error('''
                We could not find a product for such an input combination :( 
                Please re-check the input condition or parameters!
                ''')
            else:
                # final_prods_res = ', '.join(final_prods)
                st.success(f'''The product(s) for the above configuration is/are ''')
                # st.write(pd.DataFrame(final_dict).T)
                st.write(final_df)

st.title('Boiler Product Selector')
st.sidebar.title('Authentication')
uname = st.sidebar.text_input('Username')
passw = st.sidebar.text_input('Password', type="password")
auth_sbmt = st.sidebar.button('Submit')
if auth_sbmt:
    if uname in users:
        if passw == users[uname]:
            st.success(f'Logged in as {uname}')
            st.balloons()
            product_selector()
        else:
            st.sidebar.warning('User exists but password is wrong. Please re-check your password')
            st.warning('Login Failed! Try again')
    else:
        st.sidebar.error('User does not exist! Please contact the admin to add you as a user')
else :
    st.info('Please login to continue')
