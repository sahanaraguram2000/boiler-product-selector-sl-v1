import streamlit as st
import numpy as np
import pandas as pd
from constants import *
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import metrics


dset = pd.read_csv('decision_tree_v2.csv')

def compareList(l1, l2):
    return [i==j for i, j in zip(l1, l2)]
# ---------------------------------------------------------------------------------
# Internal Function which takes all the inputs for the Interal treatment - Only used for Multiple products
# ---------------------------------------------------------------------------------

def internal_function(func_type):
    st.markdown("## Internal Treatment")
    # internal = st.radio('Is an Internal Treatment product only required ?', ('Yes','No'), index=0)
    internal = 'Yes'
    if func_type == 'Multi Functional (Internal + Amine + O2)' or func_type == 'Multi Functional (Internal + Defoamer)':
        po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ['Yes'])
    else:
        po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ('Yes','No'), index=0)
    return (internal, po4)

# ---------------------------------------------------------------------------------
# Amine Function which takes all the inputs for the Amine treatment - Only used for Multiple products
# ---------------------------------------------------------------------------------

def amine_function(func_type):
    st.markdown("## Neutralizing amine")
    # n_amine = st.radio('Is Neutralizing Amine treatment required for steam and condensate treatment?', ('Yes','No'), index=0)
    n_amine = 'Yes'
    yellow = st.radio('Is there Yellow metal in the system?', ['Yes', 'No'], index=0)
    if yellow == 'No':
        dset['Q']=dset['Q'].replace({1:0})
    if func_type == 'Multi Functional (Internal + Amine + O2)':
        dr = st.selectbox('Distribution ratio', ['< 2.4'])
    else:
        dr = st.selectbox('Distribution ratio', ['< 2.4', '> 2.4'], index=0)
    return (n_amine, yellow, dr)

# ---------------------------------------------------------------------------------
# Defoamer Function which takes all the inputs for the Defoamer treatment - Only used for Multiple products
# ---------------------------------------------------------------------------------


def defoamer_function(func_type):
    # st.markdown("## Defoamer")
    # defoamer = st.radio('Is a Defoamer required ?', ('Yes','No'), index=1)
    defoamer = 'Yes'
    return defoamer
# ---------------------------------------------------------------------------------
# Oxygen Function which takes all the inputs for the Oxygen Scavenger treatment - Only used for Multiple products
# ---------------------------------------------------------------------------------

def ox_scav_function(func_type,solid_req):
    st.markdown("## Oxygen Scavengers")
    # ox_scav = st.radio('Is Oxygen Scavenger required ?', ('Yes','No'), index=0)
    ox_scav = 'Yes'
    if func_type == 'Multi Functional (Internal + Amine + O2)':
        passivation = st.radio('Is Passivation Required?', ['No'])
    elif func_type == 'Multi Functional (Amine + O2)':
        passivation = st.radio('Is Passivation Required?', ['Yes'])
    else:
        passivation = st.radio('Is Passivation Required?', ('Yes','No'), index=1)
    if (solid_req == 'Solid') or (func_type == 'Multi Functional (Internal + Amine + O2)'):
        contains_cat = st.radio('Is a product that contains catalyst required ?', ['No'])

    else:
        contains_cat = st.radio('Is a product that contains catalyst required ?', ('Yes','No'), index=1)
    return (ox_scav, passivation, contains_cat)

# --------------------------------------------
# The main product selector function which contains the entire logic of the app.
# --------------------------------------------

def product_selector():
    submit_button=None
    #OPCO
    opco = st.selectbox('Operating Country (OPCO)', ['USA','China','RSA','LATAM','Canada','EMEA'], index=0)
    col1, col2 = st.columns(2)
    opco_pres_1 = col1.slider('Operating Pressure (bar)',min_value=0, max_value=60)
    if opco_pres_1 < 10:
        op_pres = 'Less than 60 Bar'
    else:
        op_pres = 'Between 10 to 60 Bar'
        dset['G'] = dset['G'].replace({1:2})
    opco_pres_2 = opco_pres_1*14.5
    col2.metric(label="Operating pressue (psig)", value=str(opco_pres_2)+ " psig", delta_color="off")

    # Water quality
    fw = st.selectbox('Feed Water Quality', ('All (Raw/RO/Softened/Demin)', 'Raw/RO/Softened'), index=0)
    if fw=='Raw/RO/Softened':
        dset['H'] = dset['H'].replace({1:2})

    # FDA
    fda = st.radio('Is an FDA approved product for direct food application required? ',('Yes','No'))
    if fda == 'No':
        dset['I'] = dset['I'].replace({0:1})
        fda = 'Yes'

    # Dairy
    dairy = st.radio('Is it for Dairy application ?', ('Yes','No'), index=0)
    if dairy == 'No':
        dset['J'] = dset['J'].replace({0:1})
        dairy = 'both'

    # Function type
    func_type = st.selectbox('Type of function required',(
        '---------',
        'Multi Functional (Internal + Amine + O2)',
        'Multi Functional (Amine + O2)',
        'Multi Functional (Internal + Defoamer)',
        'Single Functional Products'
    ),index=0)

    # -------------------------------------------------
    # Multi Functional (Internal + Amine + O2)
    # -------------------------------------------------

    if func_type=='Multi Functional (Internal + Amine + O2)':
        sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0)
        
        defoamer = 'No'
        internal,po4 = internal_function(func_type='Multi Functional (Internal + Amine + O2)')
        n_amine, yellow, dr = amine_function(func_type='Multi Functional (Internal + Amine + O2)')
        ox_scav, passivation, contains_cat = ox_scav_function(func_type='Multi Functional (Internal + Amine + O2)',solid_req=sl)
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

    # -------------------------------------------------
    # Multi Functional (Amine + O2)
    # -------------------------------------------------

    if func_type=='Multi Functional (Amine + O2)':
        sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0)

        internal = 'No'
        po4 = 'No'
        defoamer = 'No'
        n_amine, yellow, dr = amine_function(func_type = 'Multi Functional (Amine + O2)')
        ox_scav, passivation, contains_cat = ox_scav_function(func_type = 'Multi Functional (Amine + O2)',solid_req=sl)
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

    # -------------------------------------------------
    # Multi Functional (Internal + Defoamer)
    # -------------------------------------------------
            
    if func_type=='Multi Functional (Internal + Defoamer)':
        sl = st.radio('Is a Solid/Liquid product required?', ['Liquid'])
        n_amine = 'No'
        yellow = "No"
        dr = "Not Applicable"
        ox_scav = 'No'
        passivation = 'No'
        contains_cat = 'No'
        internal,po4 = internal_function(func_type='Multi Functional (Internal + Defoamer)')
        defoamer = defoamer_function(func_type='Multi Functional (Internal + Defoamer)')
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

        # ---------------------------------------------
        # Internal for single function
        # ---------------------------------------------

        st.markdown("## Internal Treatment")
        internal = st.radio('Is Internal treatment required?', ('Yes','No'), index=1)
        if internal == 'Yes':
            sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0, key='1')
            if sl == 'Solid':
                if dairy == 'Yes':
                    po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ['Yes'])
                else:
                    po4 = st.radio('Is Phosphate (PO4) allowed in the product ?', ['Yes','No'])
            else:
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

        # ---------------------------------------------
        # amine for single function
        # ---------------------------------------------

        st.markdown("## Neutralizing amine")

        n_amine = st.radio('Is Neutralizing Amine treatment required for steam and condensate treatment?', ('Yes','No'), index=1)
        if n_amine == 'Yes':
            if dairy == 'Yes':
                st.warning("💡: Neutralizing Amine products can not be used for dairy applications. Please recheck the question 'Is it for Dairy application ?' ")
            sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0, key='2')
            yellow = st.radio('Is there Yellow metal in the system?', ['Yes', 'No'], index=0)
            if yellow == 'No':
                dset['Q']=dset['Q'].replace({1:0})
            if sl =='Solid':
                dr = st.selectbox('Distribution ratio', ['< 2.4'])
            else:
                dr = st.selectbox('Distribution ratio', ['> 2.4'])
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

        # ---------------------------------------------
        # Defoamer for single function
        # ---------------------------------------------

        st.markdown("## Defoamer")
        defoamer = st.radio('Is a Defoamer required ?', ('Yes','No'), index=1)
        if defoamer == 'Yes':
            sl = st.radio('Is a Solid/Liquid product required?', ['Liquid'])
            # sl = 'Liquid'
            if opco not in ['USA','Canada','LATAM']:
                st.warning('There is no single functional defoamer available for your OPCO. Please re-check your input conditions or select a Multifunctional (Internal + Defoamer) Product.')
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

        # ---------------------------------------------
        # Oxygen scavenger for single function
        # ---------------------------------------------

        st.markdown("## Oxygen Scavengers")
        ox_scav = st.radio('Is Oxygen Scavenger required ?', ('Yes','No'), index=1)
        passivation='No'
        contains_cat = 'No'
        if ox_scav=='Yes':
            sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0,key='4')
            # passivation = st.radio('Is Passivation Required?', ('Yes','No'), index=1)
            if sl == 'Solid':
                contains_cat =  st.radio('Is a product that contains catalyst required?', ['No'])
                passivation = st.radio('Is Passivation Required?', ['Yes'])

            else:
                contains_cat =  st.radio('Is a product that contains catalyst required?', ['Yes'])
                passivation = st.radio('Is Passivation Required?', ['No'])
                # contains_cat = st.radio('Is a product that contains catalyst required?', ('Yes','No'), index=1)
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
        
        
        # Adding Alkalinity Booster 

        st.markdown("## Alkalinity Booster")
        alk_dict={
            'selected':'No',
            'product':["No product found or the treatment was not selected"]
        }
        alk_booster = st.radio('Is Alkalinity Booster required ?', ('Yes','No'), index=1)
        if alk_booster == 'Yes':
            sl = st.radio('Is a Solid/Liquid product required?', ('Solid','Liquid'), index=0,key='5')
            if (sl == 'Solid') and (opco in ['USA','Canada', 'LATAM', 'RSA']) and (op_pres=='Between 10 to 60 Bar') and (fw == 'All (Raw/RO/Softened/Demin)') and (fda == 'Yes') and (dairy == 'both'):
                alk_dict['selected'] = 'Yes'
                alk_dict['product'] = ['Impackt BW ALK']
            elif (sl == 'Liquid')  and (opco in ['Canada']) and (op_pres=='Between 10 to 60 Bar') and (fw == 'All (Raw/RO/Softened/Demin)') and (fda == 'Yes') and (dairy == 'both'):
                alk_dict['selected'] = 'Yes'
                alk_dict['product'] = ['BLB9593']
            else:
                pass
        submit_button = st.button(label='Submit')

        




    if submit_button:
        X = dset.drop(columns=['V'])
        y = dset['V']
        X_train = X
        y_train = y
        clf = tree.DecisionTreeClassifier(max_depth=100)
        clf.fit(X_train,y_train)

        # -----------------------------------------------------------------------------
        # Dealing with Xtrain Ytrain separately with respect to each function type
        # Multifunctional : Only one product predictions
        # Single function: Multiple product predictions (max 4 types)
        # -----------------------------------------------------------------------------


        if func_type !='Single Functional Products':
            # -----------------------------------------------------------------------------
            # Everything but single functional product will come here
            # -----------------------------------------------------------------------------
            print('Len of val is', len(valv))
            X_list = X.values.tolist()
            msg = None
            prod = None
            err = None
            change_params = []
            print('*************************')
            for item in X_list:
                if all(compareList(item,valv)):
                    valv_df = pd.DataFrame(valv).transpose()
                    valv_df.columns = X.columns
                    pred_ui = clf.predict(valv_df)
                    print(pred_ui)
                    prod = pred_ui
                elif sum(compareList(item,valv))>18:
                    print(sum(compareList(item,valv)))
                    cmp_list = compareList(item,valv)
                    change_index = [i for i, x in enumerate(cmp_list) if not x]
                    # and (i in range(0,10))
                    change_params = change_params + [change_dict[i] for i in change_index if (change_dict[i] not in change_params)]
                    # st.write(change_index)
                    # change_params = change_params + [change_dict.get(i) for i in change_index if i not in change_params]
                    msg = f'We do not have a product for the given combination. But, changes in the following questions can lead to a product'
                else:
                    err = 'No products found'
            if prod :
                st.success(f'The product for the above configuration is/are {prod[0]}')
                st.info(f'{desc_dict[prod[0]]}')
            elif msg:
                st.warning(msg)
                st.write(pd.DataFrame({
                    'Questions':list(set(change_params))
                }, index=None))
            else:
                st.error(err)
        else:
            # st.write(master_list)
            final_prods = list()
            final_prods_keys = [
                'Internal treatment',
                'Neutralizing amine',
                'Defoamer',
                'Oxygen Scavengers',
                'Alkalinity Booster'
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
                        final_prods.extend(['No product found or the treatment was not selected'])
                        # st.write(f'found {key}')
                else:
                    final_prods.extend(['No product found or the treatment was not selected'])
            final_prods.extend(alk_dict['product'])
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
                for prod in final_prods:
                    if prod != 'No product found or the treatment was not selected':
                        st.info(f"{prod} : {desc_dict.get(prod)}")

st.title('Boiler Product Selector')
st.sidebar.title('Authentication')
uname = st.sidebar.text_input('Username')
passw = st.sidebar.text_input('Password', type="password")
auth_sbmt = st.sidebar.checkbox('Login')
if auth_sbmt:
    if uname in users:
        if passw == users[uname]:
            st.info(f'Logged in as {uname}')
            # st.balloons()
            product_selector()
        else:
            st.sidebar.warning('User exists but password is wrong. Please re-check your password')
            st.warning('Login Failed! Try again')
    else:
        st.sidebar.error('User does not exist! Please contact the admin to add you as a user')
else :
    st.info('Please login to continue')




    

   
