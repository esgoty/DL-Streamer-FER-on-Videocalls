import streamlit as st
from pinotdb import connect
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
from math import pi
from datetime import date
import numpy as np
from datetime import datetime, timedelta



def map_valence_activ (df_subject):
            # Create a figure and axes
            fig, ax = plt.subplots()

            plt.xlim(-1.2, 1.2)
            plt.ylim(-1.2, 1.2)

            # Define the list of words
            word_list = ['Neutral', 'Happy', 'Delighted', 'Excited', 'Tense', 'Angry',
                        'Frustrated', 'Depressed', 'Bored', 'Tired', 'Calmed', 'Relaxed', 'Content']
            

            # Create a pandas DataFrame
            data = {'word': word_list, 'radius': 0.001}
            df = pd.DataFrame(data)

            emociones_call = df_subject['emotion'].value_counts() 
            emociones_call_rel = emociones_call / (df_subject.shape[0])

            #st.write(emociones_call_rel)

            for index, value in emociones_call_rel.items():
                matching_row = df[df["word"].str.lower() == index.lower()]
                if not matching_row.empty:
                    df.loc[matching_row.index, "radius"] = value


            # Number of bubbles (excluding the center one)
            num_bubbles = len(df) - 1

            # Set the distance from the origin for the bubbles
            distance_from_center = 0.6

            # Generate random angles for the bubbles
            angles = np.linspace(0, 2 * np.pi, num_bubbles, endpoint=False)

            # Calculate the x and y coordinates for the bubbles on the circle
            x_bubble_centers = distance_from_center * np.cos(angles + 0.24)
            y_bubble_centers = distance_from_center * np.sin(angles + 0.24)

            # Create the scatter plot with sizes based on DataFrame 'radius' column
            scatter_plot = plt.scatter(x_bubble_centers, y_bubble_centers, s=df['radius'][1:] * 1000, alpha=0.7, color='blue')

            # Add text labels to the bubbles using DataFrame 'word' column
            for i, (x, y, radius, label) in enumerate(zip(x_bubble_centers, y_bubble_centers, df['radius'][1:], df['word'][1:])):
                angle = np.arctan2(y, x)
                x_label = x + 0.3 * np.cos(angle)
                y_label = y + 0.3 * np.sin(angle)

                plt.text(x_label, y_label, label, ha='center', va='center', fontsize=10)

            # Add the center bubble with a label
            plt.scatter(0, 0, s=df['radius'][0] * 1000, alpha=0.7, color='blue')
            plt.text(0.1, 0.1, df['word'][0], ha='center', va='center', fontsize=10)

            # Configure plot elements
            plt.axis('off')
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)


            # Add a line parallel to the x-axis
            plt.axhline(y=0, color='black', linestyle='--', linewidth=0.7)
            plt.axvline(x=0, color='black', linestyle='--', linewidth=0.7)

            plt.text(-0.3, 1.3, 'Activación', ha='center', va='center', fontsize=14) 

            plt.text(1.3, 0.08, 'Valencia', ha='center', va='center', fontsize=14) 

            plt.legend()

            # Display the plot in Streamlit
            st.pyplot(fig)
            

def calc_timelapse(df_subject):
            # Determine the desired bin size (se hacen bins de 1 minuto 0 60 segundos)
            # CAMBIAR A 60 !!!!!!!!!!
            bin_size = 5
            bin_edges = np.arange(df_subject['timestamp'].min() // bin_size * bin_size, df_subject['timestamp'].max() + bin_size, bin_size)

            # Calculate bin edges
            def bincounting (quadrant_str):               
                filtered_df = df_subject[df_subject['emotion_quadrant'] == quadrant_str]
                # Create a new series with binned values
                binned_data = pd.cut(filtered_df['timestamp'], bins=bin_edges, labels=False, right=False)
                # Count occurrences in each bin
                bin_counts = binned_data.value_counts()
                return bin_counts

            df = pd.DataFrame(bin_edges,columns=['Time'])
            df['positive'] = bincounting('positive')
            df['negative'] = bincounting('negative')
            df['neutral'] = bincounting('neutral')

            return df.fillna(0)



def map_time_spread ( df_sujeto ): 
    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot the lines
    sns.lineplot(x='Time', y='positive', data=calc_timelapse(df_sujeto), label='Positive', ax=ax)
    sns.lineplot(x='Time', y='negative', data=calc_timelapse(df_sujeto), label='Negative', ax=ax)
    sns.lineplot(x='Time', y='neutral', data=calc_timelapse(df_sujeto), label='Neutral', ax=ax)

    # Set plot title and labels
    plt.title('Time Series Plot')
    plt.xlabel('Time')
    plt.ylabel('Detecciones por cuadrante')
    plt.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)





def balpark_balance ( df_sujeto1 , df_sujeto2):

    sujeto1_common_emotion = df_sujeto1['emotion_quadrant'].value_counts().idxmax()
    sujeto2_common_emotion = df_sujeto2['emotion_quadrant'].value_counts().idxmax()


    if sujeto1_common_emotion == 'positive' and sujeto2_common_emotion == 'positive':
        st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                Mostly positive")  
        
    elif sujeto1_common_emotion == 'negative' and sujeto2_common_emotion == 'negative':
        st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                Mostly negative") 
         
    elif sujeto1_common_emotion != sujeto2_common_emotion :
        st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                Mixed experience")  
    
    elif sujeto1_common_emotion == 'neutral' and sujeto2_common_emotion == 'neutral':
        st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\
                Mostly Neutral") 


def emotion_mapping(emotion_label):
    positive_emotions = {'happy', 'surprise'}
    negative_emotions = {'sad', 'angry', 'fear'}
    
    if emotion_label in positive_emotions:
        return 'positive'
    elif emotion_label in negative_emotions:
        return 'negative'
    return 'neutral'



#####  Obtener todas las ID disponibles
broker_port = 8099
conn = connect(host='172.19.0.5', port=broker_port, path='/query/sql', scheme='http')

query = f"""
SELECT DISTINCT tags
FROM movies
LIMIT 300;
"""
curs = conn.cursor()
curs.execute(query)

availablerecords = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

############################################## Defino y corro APP streamlit
st.image("logo-no-background.svg", caption="Detección, estimación y cuantificación de lenguaje no verbal en videollamadas.", width=150)

# Comandos para setar globales
st.title("Call's Summary")


option = st.selectbox(
    "List of available RECORDS", availablerecords['tags'].tolist(), index=None,
   placeholder="Select the record...", label_visibility="hidden"
)


if option==None:
    st.write("### Nothing to show here")
if option!=None:
    broker_port = 8099
    conn = connect(host='172.19.0.5', port=broker_port, path='/query/sql', scheme='http')

    query = f"""
        SELECT *
        FROM movies
        WHERE tags = '{option}'
        LIMIT 10000;
    """ 
    curs = conn.cursor() 
    curs.execute(query)


    # Acondicionamiento del Dataframe 
    chart_data = pd.DataFrame(curs, columns=[item[0] for item in curs.description]).sort_values(by='timestamp')
    chart_data['timestamp'] = chart_data['timestamp']/1000000000 
    chart_data.sort_values(by=['timestamp'], inplace=True)
    chart_data['tags'] = chart_data['tags'].apply(lambda x: [x[0]])


    with st.container():
        st.markdown("## Session details")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Agent Name:** Santiago Paz  ")

            fechahorainicio=datetime.strptime(option, '%Y%m%d%H%M%S') 

            fechahorainicio_str = fechahorainicio.strftime('%Y-%m-%d %H:%M:%S')
            st.markdown(f"**Start date & time:** {fechahorainicio_str} ")

            fechahorafin=fechahorainicio + timedelta(seconds=int(chart_data['timestamp'].max() ))

            fechahorafin_str = fechahorafin.strftime('%Y-%m-%d %H:%M:%S')
            st.markdown(f"**Finish date & time:** {fechahorafin_str} ")

        with col2:
            st.metric("Total time", str(fechahorafin-fechahorainicio))
            # Todo eso tiene que venir de la base de datos...
            # o parseas la tag, o agregas columnas. 
            st.write("#")

    with st.container():

        st.markdown("## Session result")

        new_df = chart_data[["emotion", "emotion_confidence", "xcord","ycord"]]

        sujeto1 = new_df.apply(lambda x: x.str[0] if isinstance(x, pd.Series) and x.dtype == 'object' else x)
        sujeto1['tags']=chart_data['tags']
        sujeto1['timestamp']=chart_data['timestamp']
        sujeto1['emotion_quadrant']= sujeto1['emotion'].map(emotion_mapping)

        #sujeto1['emotion_quadrant'].iloc[5] ='neutral'

        #for i in range(200, 241):
        #    sujeto1['emotion_quadrant'].iloc[i] = 'negative'

        sujeto2 = new_df.apply(lambda x: x.str[1] if isinstance(x, pd.Series) and x.dtype == 'object' else x)
        sujeto2['tags']=chart_data['tags']
        sujeto2['timestamp']=chart_data['timestamp']
        sujeto2['emotion_quadrant']= sujeto2['emotion'].map(emotion_mapping)


        balpark_balance(sujeto1,sujeto2)
        st.markdown("#")


    with st.container():  
        st.markdown("## Summary Subject 1")


        col1, col2 = st.columns(2)

        with col1:
            map_valence_activ(sujeto1)

        with col2:
            map_time_spread ( sujeto1 )          
            st.markdown("#")

    with st.container():  
        st.markdown("## Summary Subject 2")


        col1, col2 = st.columns(2)

        with col1:
            map_valence_activ(sujeto2)

        with col2:
            map_time_spread ( sujeto2 )
            




    with st.container():
        st.markdown("# ")
        st.markdown("## Wiki Valence-Arousal")
        with st.expander("Know more about Valence-Arousal Space"):
            st.markdown('''
                The "valence-arousal space" is a way of describing and understanding emotions based on two main dimensions: valence and arousal.\n
                **Valence:** This dimension describes whether an emotion feels positive or negative. Emotions with positive valence make us feel good, like happiness or excitement. Emotions with negative valence make us feel bad, like sadness or fear. \n
                **Arousal:** This dimension describes the intensity or energy level of an emotion. Emotions with high arousal are intense and can make us feel more active or energized, like excitement or anger. Emotions with low arousal are more subdued and calm, like relaxation or contentment. \n
            ''')
            st.image('/home/santi/Documents/TP-FINAL-CEIA/Recursos/REPORTING/App-streamlit/va_space.png')
            st.markdown('''
                Hsu, Lun-Kai & Tseng, Wen-Sheng & Kang, Li-Wei & Wang, Yu-Chiang Frank. (2013). Seeing through the expression: Bridging the gap between expression and emotion recognition. Proceedings - IEEE International Conference on Multimedia and Expo. 1-6. 10.1109/ICME.2013.6607638. 
            ''')      
    