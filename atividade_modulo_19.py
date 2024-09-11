import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st
from PIL import Image
from io import BytesIO


#sns.set_style('whitegrid')
st.set_page_config(page_title= 'Telemarketing',
            page_icon=(r'.\Material_de_apoio_M19_Cientista de Dados\img\telmarketing_icon.png'),
            layout = 'centered',
            initial_sidebar_state= 'expanded',
                )

image = Image.open(r"..\Atividade 1\Material_de_apoio_M19_Cientista de Dados\img\Bank-Branding.jpg")
st.sidebar.image(image)

st.title('Telemarketing Análises')

st.cache_data(show_spinner = True)
def col_all(df , col) -> list:
     lista = df[col].unique().tolist()
     lista.append('All')

     return lista

st.cache_data(show_spinner = True)
def multiselect_filter(df , col , selecionados):
     if 'All' in selecionados:
          return df
     
     else:
        df_filtrado = df[df[col].isin(selecionados)].reset_index(drop = True)
     
     return df_filtrado

st.cache_data()
def open_file(path) -> pd.DataFrame:
    DataFrame = pd.read_csv(path , sep = ';' , encoding = 'utf-8')

    return DataFrame

@st.cache_data()
def convert_df(df):
    
    return df.to_csv(index=False).encode('utf-8')


@st.cache_data()
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    
    return processed_data



data = st.sidebar.file_uploader('Bank data' , type = ['csv' , 'xlsx'])


if (data is not None):
    df = open_file(data)
               
    def main():
        
        st.subheader('Dados Originais' , divider= 'red')
        df_copy = df.copy()

        st.write(df.head())


        #FILTROS
        with st.sidebar.form(key='my_form'):

            st.write('FILTROS')

            #Filtro idade 

            max_idade = int(df.age.max())
            min_idade = int(df.age.min())

            idades = st.slider(label= 'Idade',
                                    min_value= min_idade,
                                    max_value= max_idade,
                                    value=(min_idade , max_idade),
                                    step= 1
                                    )
            #Filtro trabalho
            jobs_list = col_all(df , 'job')
            jobs_selected = st.multiselect('Profissões' , jobs_list , 'All')
            #Filtro dia da semana
            days_list = col_all(df , 'day_of_week')
            days_selected = st.multiselect('Dias da semana' , days_list , 'All')
            #Filtro educação
            education_list = col_all(df , 'education')
            education_selected = st.multiselect('Educação' , education_list , 'All')
            #Filtro Default
            default_list = col_all(df , 'default')
            default_selected = st.multiselect('Default' , default_list , 'All')
            #Filtro mensal
            month_list = col_all(df , 'month')
            month_selected = st.multiselect('Mês' , month_list , 'All')
            #Filtro matrimonial
            marital_list = col_all(df , 'marital')
            marital_selected = st.multiselect('Matrimonio' , marital_list , 'All')
            #Filtro habitação
            housing_list = col_all(df , 'housing')
            housing_selected = st.multiselect('Habitação' , housing_list , 'All')
            #Filtro contato
            contact_list = col_all(df , 'contact')
            contact_selected = st.multiselect('Contato' , contact_list , 'All')
            #Filtro emprestimo
            loan_list = col_all(df , 'loan')
            loan_selected = st.multiselect('Emprestimo' , loan_list , 'All')

            df_copy = (df_copy.query("age >= @idades[0] and age <= @idades[1]")
                        .pipe(multiselect_filter, 'job', jobs_selected)
                        .pipe(multiselect_filter, 'marital', marital_selected)
                        .pipe(multiselect_filter, 'default', default_selected)
                        .pipe(multiselect_filter, 'housing', housing_selected)
                        .pipe(multiselect_filter, 'loan', loan_selected)
                        .pipe(multiselect_filter, 'contact', contact_selected)
                        .pipe(multiselect_filter, 'month', month_selected)
                        .pipe(multiselect_filter, 'day_of_week', days_selected)
                        .pipe(multiselect_filter, 'education', education_selected)
            )
 
            tipo_grafico = st.radio('Tipo de gráfico' , ('Barras' , 'Pizza'))
            submit_buton = st.form_submit_button(label = 'Aplicar')

        st.write('## Após os filtros')
        st.write(df_copy.head())
        
        df_xlsx = to_excel(df_copy)
        st.download_button(label='📥 Download tabela filtrada em EXCEL',
                            data=df_xlsx ,
                            file_name= 'bank_filtered.xlsx')
        
        st.subheader('Gráficos')

        #Plots

        fig , ax = plt.subplots(1 , 2 , figsize=(15 , 8))
        
        df_perc = df.y.value_counts(normalize = True).to_frame() * 100
        df_perc = df_perc.sort_index()

        df_copy_perc = df_copy.y.value_counts(normalize=True).to_frame() * 100
        df_copy_perc = df_copy_perc.sort_index()

        if tipo_grafico == 'Barras':
             
            sns.barplot(x = df_perc.index , 
                        y = 'proportion',
                        data = df_perc,
                        ax = ax[0]
                        )

            ax[0].bar_label(ax[0].containers[0])
            ax[0].set_title('Dados brutos',
                        fontweight = 'bold')

            sns.barplot(x = df_copy_perc.index , 
                        y = 'proportion' , 
                        data = df_copy_perc ,
                        ax = ax[1])

            ax[1].bar_label(ax[1].containers[0])
            ax[1].set_title('Dados filtrados' , 
                            fontweight = 'bold')


            st.pyplot(plt)
        else:

            df_perc.plot(kind='pie', autopct='%.2f', y='proportion', ax = ax[0])
            ax[0].set_title('Dados brutos',
                            fontweight ="bold")
            
            df_copy_perc.plot(kind='pie', autopct='%.2f', y='proportion', ax = ax[1])
            ax[1].set_title('Dados filtrados',
                            fontweight ="bold")


            st.pyplot(plt) 

    
    

    if __name__ == '__main__':
	    main()
else:
     st.write('Faça upload do arquivo para iniciar as análises')
