import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import preprocessor
import helper



st.sidebar.title("whatsapp chat processor")
uploader=st.sidebar.file_uploader("upload file", type=['txt'], accept_multiple_files= False)

if  uploader is not None:
    data=uploader.getvalue().decode('utf-8')
    
    df=preprocessor.preprocess(data)
    v1= st.title("whatsapp chat")
    v2= st.dataframe(df)

    user_list= df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()

    v3= st.header("total members")
    v4= st.title(len(user_list))


    user_list.insert(0,"overall")



    selected_user=st.sidebar.selectbox("chat analysis",user_list)

    if st.sidebar.button('show analysis'):
        
        v1.empty()
        v2.empty()
        v3.empty()
        v4.empty()

        user_df= helper.dataframe(selected_user, df)
        st.title("selected user's chats")
        st.dataframe(user_df)
        
        st.title("Selected user's Statistic")
        num_messages, words, num_media, links = helper.fetch_stats(selected_user,df)

        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("total messages")
            st.title(num_messages)

        with col2:
            st.header("total words")
            st.title(words)

        with col3:
            st.header("total media")
            st.title(num_media)

        with col4:
            st.header("total links")
            st.title(links)

        st.title("monthly timeline")
        timeline_df= helper.monthly_timeline(selected_user, df)
        fig, ax= plt.subplots()
        plt.scatter(timeline_df['time'],timeline_df['message'])
        plt.xlabel("month")
        plt.ylabel("frequency of message")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("daily timeline")
        daily_timeline_df= helper.daily_timeline(selected_user, df)
        fig, ax= plt.subplots()
        plt.scatter(daily_timeline_df['date'],daily_timeline_df['message'], color='black')
        plt.xlabel("days")
        plt.ylabel("frequency of message")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("activity map")
        col1, col2= st.columns(2)

        with col1:
            st.header('most busy day')
            busy_day=helper.weekly_activity(selected_user, df)

            fig, ax= plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            plt.xlabel("day")
            plt.ylabel("frequency of message")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header('most busy month')
            busy_month=helper.month_activity(selected_user, df)

            fig, ax= plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xlabel("month")
            plt.ylabel("frequency of message")
            plt.xticks(rotation=45)
            st.pyplot(fig)


        if selected_user =='overall':
            st.title('most busy users')
            
            x, new_df=helper.most_busy_user(df)
            fig, ax= plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xlabel("users")
                plt.ylabel("frequency of message")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)



        st.title('Wordcloud')
        df_wc= helper.create_wordcloud(selected_user, df)
        fig, ax= plt.subplots()
        ax.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)

        st.title('most common words')
        common_df= helper.most_common_words(selected_user,df)

        col1,col2 = st.columns(2)

        with col1:
             fig, ax= plt.subplots()
             ax.bar(common_df[0], common_df[1])
             plt.xlabel("common words")
             plt.ylabel("frequency of words")
             st.pyplot(fig)

        with col2:
            st.dataframe(common_df)
        
        
        st.title('common emoji used')
        emoji_df = helper.show_emoji(selected_user,df)
        
        
    
        col1,col2 = st.columns(2)
            
        with col1:
            st.dataframe(emoji_df)
                
        with col2:
            fig, ax= plt.subplots()
            ax.pie(emoji_df[1], labels= emoji_df[0])
            plt.legend(emoji_df[0], loc ="best")
            st.pyplot(fig)

        
        