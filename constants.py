
# Users are put here in the format of 'username':'password'
users = {
    'Firestorm':'Buckman123'
}

# Change request 
change_dict = {
    0:'OPCO',
    1:'OPCO',
    2:'OPCO',
    3:'OPCO',
    4:'OPCO',
    5:'OPCO',
    6:'Operating Pressure (bar)',
    7:'Feed water quality',
    8:'Is an FDA approved product for direct food application required?',
    9:'Is it for Dairy application ?',
    10:'Type of function required',
    11:'Is a Solid/Liquid product required?',
    12:'Is Internal treatment required?',
    13:'Is Phosphate (PO4) allowed in the product ?',
    14:'Is a Defoamer required ?',
    15:'Is Neutralizing Amine treatment required for steam and condensate treatment?',
    16:'Is there Yellow metal in the system?',
    17:'Distribution ratio',
    18:'Is Oxygen Scavenger required ?',
    19:'Is Passivation Required?',
    20:'Is a product that contains catalyst required?',
}




#Encoders are put here
opco_dict = {
    'USA' : [1,0,0,0,0,0],
    'China' : [0,1,0,0,0,0],
    'RSA' : [0,0,1,0,0,0],
    'LATAM' : [0,0,0,1,0,0],
    'Canada' : [0,0,0,0,1,0],
    'EMEA' : [0,0,0,0,0,1]
}
op_pres_dict={
    'Less than 60 Bar': 1,
    'Between 10 to 60 Bar': 2
}


fw_dict = {
    'All (Raw/RO/Demineralized)':1, # 1 -> All(Raw/Ro/Demin)
    'Raw, RO Only':2 #2 -> Raw and RO only
}

fda_dict ={
    'Yes':1,
    'No':0
}
dairy_dict = {
    'Yes':1,
    'No':0,
    'both':1
}

func_type_dict = {
    'Multi Functional (Internal + Amine + O2)':1,
    'Multi Functional (Amine + O2)':3,
    'Multi Functional (Internal + Defoamer)':2,
    'Single Functional Products':4
}
sl_dict = {
    'Solid':1,
    'Liquid':2
}
internal_dict = {
    'Yes':1,
    'No':0
}
po4_dict = {
    'Yes':1,
    'No':0
}
defoamer_dict = {
    'Yes':1,
    'No':0
}
n_amine_dict = {
    'Yes':1,
    'No':0
}
yellow_dict = {
    'No':0,
    'Yes':1,
}
dr_dict = {
    '< 2.4':1,
    '> 2.4':2,
    'Not Applicable':3
}

ox_scav_dict = {
    'Yes':1,
    'No':0
}

contains_cat_dict = {
    'Yes':1,
    'No':0
}

passivation_dict = {
    'Yes':1,
    'No':0
}
