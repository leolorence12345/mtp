import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image

# Display Title and Description
st.title("Snake Bite Management Portal")

# Constants
LOCATION_OPTIONS = {
    "DARJEELING": [6, 1, 1, 2],
    "KALIMPONG": [6, 1, 1, 2],
    "JALPAIGURI": [1, 5, 1, 3],
    "ALIPURDUAR": [1, 5, 1, 3],
    "COOCHBEHAR": [4, 2, 2, 2],
    "MALDA": [1, 4, 2, 3],
    "UTTAR DINAJPUR": [3, 3, 2, 2],
    "DAKSHIN DINAJPUR": [2, 5, 2, 1],
    "MURSHIDABAD": [2, 3, 2, 3],
    "BIRBHUM": [4, 1, 2, 3],
    "HOOGHLY": [2, 3, 3, 2],
    "PASHCHIM BARDHAMAN": [1, 3, 4, 2],
    "PURBA BARDHAMAN": [1, 3, 3, 3],
    "BANKURA": [1, 4, 3, 2],
    "JHARGRAM": [1, 4, 3, 2],
    "PURULIA": [1, 4, 1, 4],
    "PURBA MEDINIPUR": [3, 1, 3, 3],
    "PASHCHIM MEDINIPUR": [3, 1, 4, 2],
    "HOWRAH": [2, 4, 3, 1],
    "KOLKATA": [1, 4, 4, 1],
    "NADIA": [1, 3, 3, 3],
    "NORTH 24 PARGANAS": [2, 3, 3, 2],
    "SOUTH 24 PARGANAS": [3, 1, 3, 3],
}

TIME = {
    "Early Morning": [3, 3, 3, 3],
    "During the day": [3.5, 3.5, 8.5, 1],
    "Evening": [8.5, 8.5, 4.5, 3],
    "Night": [6.5, 7.5, 3.5, 8.5],
}


SEASON = {
    "Monsoon": [9, 9, 7, 9],
    "Autumn": [7, 8.5, 8, 8.5],
    "Winter": [5.5, 5.5, 6.5, 5.5],
    "Spring": [7, 7, 7, 7.5],
    "Summer": [9, 9, 9, 9],
}


PLACE= {
    "Indoor": [3 , 7.5 , 6, 8.5],
    "Agriculture Field (Dry)":	[5.5 , 6.5, 9,	1],
    "Agriculture Field (Wet)/Near Water Bodies": 	[9	,4,	5.5,0.5],
    "High and Dry Areas (Near Human Settlements)-Outdoor":	[5	,8.5 ,7	,2.5],

       }

LOCAL_SYMPTOMS={
    "pain": [6, 6, 8, 1],
    "swelling": [4.5, 4.5, 6.5, 1],
    "haemmorhage": [4, 4, 7, 1],
    "skin colour change": [4, 4, 8, 0.5],
    "Blisters": [4, 4, 8, 0.5],
    "No Symptoms":[0,0,0,0],
}

SYSTEMATIC_SYMPTOMS={
"drowsiness": [6, 6, 1, 6.5],
"breathing difficulty": [6.5, 6.5, 2, 6.5],
"abdominal pain/vomiting": [2, 2, 1, 8.5],
"dropping eyes (ptosis)": [7, 7, 2, 8],
"swallowing issue/burning sensation in upper chest and throat": [7, 7, 1, 8],
"haemmorhage_systematic": [0.5, 0.5, 8, 0.5],
"paralysis": [7, 7, 1, 7],
"No Symptoms":[0,0,0,0],
}

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Snake", usecols=list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")
# st.dataframe(existing_data)

action = st.selectbox(
    "Choose an Action",
    [
        "Snake Bite Detection",
        "View Snake Bite Records",
    ],
)

if action == "Snake Bite Detection":
    st.markdown("Enter the details of the snake bite incident below.")
    with st.form(key="snakebite_form"):
        # company_name = st.text_input(label="Company Name*")
        district_bite = st.selectbox("What is the location of the bite*", options= LOCATION_OPTIONS, index=None,key="district_bite") or "BIRBHUM"
        location_values = LOCATION_OPTIONS[district_bite]

        time_bite = st.selectbox("What is the time of the bite*",  options=list(TIME.keys()), index=None,key="time_bite") or "Early Morning"
        time_values = TIME[time_bite]

        season_bite = st.selectbox("What is the season during bite*", options= SEASON, index=None,key="season_bite") or "Monsoon"
        season_values = SEASON[season_bite]

        place_bite = st.selectbox("Where did the bite happen*", options= PLACE, index=None ,key="place_bite") or "Indoor"
        place_values = PLACE[place_bite]
#----------------------------------------------------------------------------------------------------------------------------------
        local_symptoms = st.multiselect("What are the local symptoms the patient is feeling*", options=list(LOCAL_SYMPTOMS.keys()) ,key="local_bite")
        local__symptom_values = {symptom: LOCAL_SYMPTOMS[symptom] for symptom in local_symptoms}
        result_local = None
        for key, values in local__symptom_values.items():
        # If result is None, initialize it with the values of the first key
            if result_local is None:
                result_local = values
            else:
                result_local = [sum(pair) for pair in zip(result_local, values)]

#----------------------------------------------------------------------------------------------------------------------------------
        systa_symptoms = st.multiselect("What are the Systematic symptoms the patient is feeling", options=SYSTEMATIC_SYMPTOMS,key="sys_bite")
        systa_symptom_values = {symptom: SYSTEMATIC_SYMPTOMS[symptom] for symptom in systa_symptoms}
        result_sys = None
        for key, values in systa_symptom_values.items():
        # If result is None, initialize it with the values of the first key
            if result_sys is None:
                result_sys = values
            else:
                result_sys = [sum(pair) for pair in zip(result_sys, values)]




        additional_info = st.text_area(label="Additional Notes")
        snake_bitten = "cobra"
        st.markdown("**required*")
        submit_button = st.form_submit_button(label="Submit Snake Bite Details")


        if submit_button:
            if not district_bite or not time_bite or not season_bite or not place_bite or not local_symptoms or not systa_symptoms:
                st.warning("Ensure all mandatory fields are filled.")
                
            else:
                
                weights = [0.8, 0.4, 0.4, 0.5,0.6,0.8]
                results = [sum(x * w for x, w in zip(index_values, weights)) for index_values in zip(location_values, time_values,season_values,place_values,result_local, result_sys)]
                total_sum = sum(results)
                probabilities = [(result / total_sum) * 100 for result in results]


                max_index = probabilities.index(max(probabilities))
                max_species = ["Monocled Cobra", 'Spectacled Cobra', "Russell's Viper", "Krait Species"][max_index]  # Replace with your actual species labels

                if local_symptoms == ["No Symptoms"] and systa_symptoms == ["No Symptoms"]:
                    st.markdown(f"**Snake Bitten :** {max_species} with no Envenomation.")
                # Display the species with the highest probability
                else:
                    st.markdown(f"**Snake Bitten :** {max_species}")

                # Load and display the image corresponding to the identified species
                species_images = {
                    "Monocled Cobra": "m.cobra.webp",
                    "Spectacled Cobra": "S.cobra.jpg",
                    "Russell's Viper": "Russells-viper.jpg",
                    "Krait Species": "krait.jpg",
                }

                max_species_image_path = species_images.get(max_species)
                if max_species_image_path:
                    max_species_image = Image.open(max_species_image_path)

                    new_width = 300
                    new_height = 300
                    resized_image = max_species_image.resize((new_width, new_height))
                    st.image(resized_image, caption=f"Image of {max_species}",width=300)




                vendor_data = pd.DataFrame(
                    [
                        {
                            "District": district_bite,
                            "Time": time_bite,
                            "Season":season_bite,
                            "Place": place_bite,
                            "Local symptoms":  ", ".join(local_symptoms),
                            "Systematic symptoms": ", ".join(systa_symptoms),
                            "Snake Bitten":snake_bitten
                        }
                    ]
                )
                			 		
                updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)
                conn.update(worksheet="Snake", data=updated_df)
                st.success("Successfully Detected")
                print(location_values, time_values,season_values,place_values,result_local, result_sys)
                print(results)
                print(probabilities)


# View All Vendors
elif action == "View Snake Bite Records":
    st.dataframe(existing_data)

