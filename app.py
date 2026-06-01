import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer 💬')

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    df = preprocessor.preprocess(data)

    # Unique Users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media, link = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics 📊")
        col1, col2,col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages 📨")
            st.title(num_messages)

        with col2:
            st.header("Total Words ✏️")
            st.title(words)
        
        with col3:
            st.header("Media Shared 📷")
            st.title(num_media)

        with col3:
            st.header("Links Shared 🔗")
            st.title(link)

        # Monthly Timeline 
        st.title('Monthly Timeline ⌛')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='purple')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Activity
        st.title("Activity Map 💻")
        c1, c2 = st.columns(2)

        with c1:
            st.header('Most Busy day')
            busy_day = helper.week_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='darkslategrey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with c2:
            st.header('Most Busy Month')
            busy_month = helper.month_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='darkslateblue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Active Duration Along day ")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Active Users
        if(selected_user == 'Overall'):
            st.title('Most Active Users')
            x,new_df = helper.active_users(df)
            fig, ax = plt.subplots()
            
            cols1, cols2 = st.columns(2)

            with cols1:
                ax.bar(x.index, x.values, color='hotpink')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with cols2:
                st.dataframe(new_df)

        # WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='teal')
        plt.xticks(rotation= 'vertical')
        
        st.title('Most Common Words')
        st.pyplot(fig)

        # Emoji 

        emojis_df = helper.emoji_count(selected_user, df)
        st.title("Emoji Count")
        
        cl1, cl2 = st.columns(2)
        
        with cl1:
            st.dataframe(emojis_df)
        with cl2:
            # Change font to make emojis visible
            plt.rcParams['font.family'] = 'Segoe UI Emoji'
            fig, ax = plt.subplots()
            ax.pie(emojis_df[1].head(), labels=emojis_df[0].head(), autopct="%0.2f%%")
            st.pyplot(fig)