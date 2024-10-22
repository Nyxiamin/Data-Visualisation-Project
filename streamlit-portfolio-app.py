import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config (must be the first Streamlit command)
st.set_page_config(page_title="Parcoursup Data Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    # Use the correct delimiter for the CSV file
    df = pd.read_csv("database.csv", delimiter=';')
    # Separate summary rows and detailed data
    df_summary = df[df['Formation'] == 'Ensemble des bacheliers']
    df_detailed = df[df['Formation'] != 'Ensemble des bacheliers']
    
    return df_summary, df_detailed


df_summary, df_detailed= load_data()

df_summary['Enseignements de spécialité'] = df_summary['Enseignements de spécialité'].str.replace(' Spécialité', '', regex=False)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Portfolio", "Parcoursup Project"])

if page == "Portfolio":
    # Title and Introduction
    st.title("Welcome to My Data Science Portfolio")

    # About Me Section
    st.header("👩‍🎓 About Me")
    me_col1, me_col2 = st.columns(2)
    with me_col1:
        st.write("I am a computer engineering student with a strong interest in data science and machine learning. I enjoy applying statistical analysis and predictive modeling to drive insights and support decision-making.")
        st.write("#### Professional Objective")
        st.write("I am looking for opportunities as a Data Analyst or Machine Learning Engineer, focusing on predictive modeling and natural language processing.")
        
    with me_col2:
        st.image("IMG_7461.jpg", width=200)  # Adjust the path and size as needed

    # Skills and Tools Section
    st.header("🛠️ Skills and Tools")
    skills_col1, skills_col2 = st.columns(2)

    with skills_col1:
        st.markdown("**Technical Skills:**")
        st.write("- Python, SQL, HTML/CSS/JavaScript")
        st.write("- Libraries: Pandas, NumPy, scikit-learn, Matplotlib, Plotly")
        st.write("- Tools: Git, Jupyter, Streamlit")
        st.write("- Cloud Platforms: AWS, GCP")

    with skills_col2:
        st.markdown("**Certifications:**")
        st.write("- Master in Data Science at EFREI Paris")
        st.write("- TOIEC English 980/990")

    # Projects Section
    st.header("📊 Projects")
    st.markdown("Here are some of my notable projects:")

    project_col1, project_col2 = st.columns(2)

    with project_col1:
        st.subheader("Predicting Patent Codes with Machine Learning")
        st.write("**Objective:** Predict patent codes using historical data.")
        st.write("**Dataset:** Collected from a partnership with LIPSTIP enterprise. Key features include CPC codes, description, and patent content.")
        st.write("**Methods:** Used classification algorithms including Logistic Regression and Random Forest.")
        st.write("**Results:** Achieved an accuracy of 78%.")
        st.markdown("[GitHub Repository](https://github.com/Nyxiamin/SF)")

    with project_col2:
        st.subheader("Analysis of Higher Education Choices")
        st.write("**Objective:** Analyze the choices of French high school graduates.")
        st.write("**Dataset:** Contains validated orientation wishes, admission proposals, and accepted proposals.")
        st.write("**Methods:** Conducted exploratory data analysis and visualizations.")
        st.write("**Results:** Key insights on trends in higher education choices.")
        st.markdown("[GitHub Repository](https://github.com/Nyxiamin/DataVis)")

    # Blog Section
    st.header("📚 My last project: A Book Search Engine")
    st.write("The main concept of our solution is to guide readers who eithers have a book they are interested in reading or who does not have book and are looking for one. If they users is already interested in a book, they would be interested in the information we would show of the book.  ")
    st.markdown("[Reader's Heaven](http://readersheaven-dcgphmfacfgyhmgs.canadacentral-01.azurewebsites.net/about_us/)")

    # Work Experience Section
    st.header("💼 Work Experience")
    work_exp_col1, work_exp_col2 = st.columns(2)

    with work_exp_col1:
        st.write("- **Data Analyst Sales Intern** at Mirakl (Nov 2024 - Present)")
        st.write("  Starting my journey as a Data Analyst Sales Intern, focusing on data analysis and supporting sales strategies.")

        st.write("- **Sales Advisor** at FNAC Ternes (Jan 2023 - Feb 2023)")
        st.write("  Advised and sold office and telephony products.")

    with work_exp_col2:
        st.write("- **Marketing Assistant** at BMF Immobilier (June - Aug 2022)")
        st.write("  In charge of managing the LinkedIn profile and enhancing communication strategies.")

        st.write("- **Project Manager/Community Manager** at Junior Entreprise SEPEFREI (Nov 2021 - June 2022)")
        st.write("  Managed projects by acting as an intermediary between clients and consultants.")


    # Education Section
    st.header("🎓 Education")
    st.write("- Master’s in Data & Artificial Intelligence, EFREI Paris (2021 - Present)")
    st.write("- Relevant Courses: Data Science, Machine Learning, Inferential Statistics")

    # Resume Section
    st.header("📄 Resume")
    st.markdown("Visit my [LinkedIn Profile](https://www.linkedin.com/in/thaisbordessoul/)")

    # Contact Section
    st.header("📞 Contact Me")
    contact_col1, contact_col2 = st.columns(2)

    with contact_col1:
        st.write("Feel free to connect with me on:")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/thaisbordessoul/)")
        st.markdown("[GitHub](https://github.com/Nyxiamin)")
        st.write("[Email](mailto:thais.bordessoul@efrei.net)")

    with contact_col2:
        contact_form = st.form(key='contact_form')
        contact_form.text_input("Your Name")
        contact_form.text_input("Your Email")
        contact_form.text_area("Message")
        contact_form.form_submit_button("Send")

    st.write("---")
    st.markdown("© 2024 Thaïs Bordessoul. All rights reserved.")

if page == "Parcoursup Project":
    
    st.title("Parcoursup Admissions from 2021 to 2023")
    
    st.write("""
        In this project, I analyze data from Parcoursup, focusing on the educational trends and choices of French high school graduates 
        from 2021 onwards. The analysis explores how various subject combinations influence their higher education applications, offers, 
        and final decisions.
    """)

    st.write("""This dataset didn't had any issues apart from the fact that I removed the word "Spécialité" at the end of the specialities name.
                There was only one point of concern: "Ensemble des bacheliers" was a set of special row containing counts of students instead of total of wishes or proposals, for each duos of specialities
                Therefore, I had to separate my dataset into two to handle these data differently.""")
    

    
    # Chapter 1: Trends Over Time
    st.header("Part 1: Trends Over Time")

    yearly_totals = df_summary.groupby('Année du Baccalauréat').agg({
        'Nombre de candidats bacheliers ayant confirmé au moins un vœu': 'sum',
        'Nombre de candidats bacheliers ayant reçu au moins une proposition d\'admission': 'sum',
        'Nombre de candidats bacheliers ayant accepté une proposition d\'admission': 'sum'
    }).reset_index()

    fig_line = px.line(yearly_totals, x='Année du Baccalauréat', 
                    y=['Nombre de candidats bacheliers ayant confirmé au moins un vœu',
                        'Nombre de candidats bacheliers ayant reçu au moins une proposition d\'admission',
                        'Nombre de candidats bacheliers ayant accepté une proposition d\'admission'],
                    title="Trends in Candidates, Offers, and Acceptances",
                    labels={'value': 'Number of Candidates', 'variable': 'Category'})
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("""
        This line chart shows how the numbers of candidates making wishes, receiving offers, and accepting admissions 
        have changed over the years. We can remark that the number of candidates was overall lower in 2022, which is confirmed by the gouvernement noting 2,2 pourcent less student this year, mainly professionnal high-school students.
    """)



    years = sorted(df_summary['Année du Baccalauréat'].unique())

    # Chapter 2: The Landscape of Choices
    st.header("Part 2: The Landscape of Choices")

    year_for_sunburst = st.radio("Select a year:", years, key="sunburst_year")
    df_year = df_summary[df_summary['Année du Baccalauréat'] == year_for_sunburst]


    def split_subjects(subject):
        return subject.split(',')

    df_year['Subject1'] = df_year['Enseignements de spécialité'].apply(lambda x: split_subjects(x)[0])
    df_year['Subject2'] = df_year['Enseignements de spécialité'].apply(lambda x: split_subjects(x)[1] if len(split_subjects(x)) > 1 else 'Single')

    min_candidates_threshold = 1000 

    df_filtered = df_year[df_year['Nombre de candidats bacheliers ayant confirmé au moins un vœu'] >= min_candidates_threshold]

    fig_sunburst = px.sunburst(df_filtered, path=['Subject1', 'Subject2'], 
                                values='Nombre de candidats bacheliers ayant confirmé au moins un vœu',
                                title=f"Subject Combinations in {year_for_sunburst}")
    fig_sunburst.update_layout(height=1000)  # Adjust the value as needed
    st.plotly_chart(fig_sunburst, use_container_width=True)

    st.write(f"""
        This sunburst chart shows the accurate distribution of subject combinations chosen by students in {year_for_sunburst}. 
        Each segment represents the number of candidates who selected that particular combination of subjects.
    """)

    year_for_bar_chart = st.radio("Select a year:", years, key="bar_chart_year")
    df_year_bar = df_summary[df_summary['Année du Baccalauréat'] == year_for_bar_chart]

    df_year_bar['Specialties'] = df_year_bar['Enseignements de spécialité'].apply(lambda x: split_subjects(x))
    df_exploded = df_year_bar.explode('Specialties')

    df_grouped = df_exploded.groupby('Specialties').agg({'Nombre de candidats bacheliers ayant confirmé au moins un vœu': 'sum'}).reset_index()

    df_filtered_grouped = df_grouped[df_grouped['Nombre de candidats bacheliers ayant confirmé au moins un vœu'] >= min_candidates_threshold]

    top_10_specialties = df_filtered_grouped.nlargest(10, 'Nombre de candidats bacheliers ayant confirmé au moins un vœu')
    fig_bar_chart = px.bar(top_10_specialties, 
                        x='Specialties', 
                        y='Nombre de candidats bacheliers ayant confirmé au moins un vœu',
                        labels={'Specialties': 'Specialty', 'Nombre de candidats bacheliers ayant confirmé au moins un vœu': 'Number of Wishes'},
                        title=f"Top 10 Most Chosen Specialties in {year_for_bar_chart}")

    fig_bar_chart.update_layout(height=600, width=1000, title_x=0.5)  # Adjust layout as needed
    st.plotly_chart(fig_bar_chart, use_container_width=True)

    st.write(f"""
        This bar chart shows the top 10 most chosen specialties based on the number of confirmed wishes made by students in {year_for_bar_chart}.
        Each bar represents a specialty and the total number of candidates who selected it.
    """)




    # Chapter 3: From Aspirations to Admissions
    st.header("Part 3: From Aspirations to Admissions")

    
    year_for_tops = st.radio("Select a year:", years, key="tops_years")
    df_year_tops = df_summary[df_summary['Année du Baccalauréat'] == year_for_tops]
    df_year_tops['Subject1'] = df_year_tops['Enseignements de spécialité'].apply(lambda x: split_subjects(x)[0])
    df_year_tops['Subject2'] = df_year_tops['Enseignements de spécialité'].apply(lambda x: split_subjects(x)[1] if len(split_subjects(x)) > 1 else 'Single')

    df_duos = df_year_tops.groupby(['Subject1', 'Subject2'])['Nombre de candidats bacheliers ayant confirmé au moins un vœu'].sum().reset_index()

    df_duos_sorted = df_duos.sort_values(by='Nombre de candidats bacheliers ayant confirmé au moins un vœu', ascending=False)

    top_10_duos = df_duos_sorted.head(10)
    st.write("Top 10 Most Popular Subject Combinations:")
    st.dataframe(top_10_duos)
    top_specialties_per_year = set()
    years = df_summary['Année du Baccalauréat'].unique()

    for year in years:
        df_year = df_summary[df_summary['Année du Baccalauréat'] == year]
        top_10_for_year = df_year.groupby('Enseignements de spécialité')['Nombre de candidats bacheliers ayant confirmé au moins un vœu'].sum().nlargest(10).index
        top_specialties_per_year.update(top_10_for_year)

    df_filtered = df_summary[df_summary['Enseignements de spécialité'].isin(top_specialties_per_year)]

    df_pivot = df_filtered.pivot(index='Année du Baccalauréat', columns='Enseignements de spécialité', values='Nombre de candidats bacheliers ayant confirmé au moins un vœu')
    fig = go.Figure()

    for column in df_pivot.columns:
        fig.add_trace(go.Scatter(x=df_pivot.index, y=df_pivot[column], mode='lines', name=column, line=dict(width=2)))

    fig.update_layout(
        title="Nombre de candidats bacheliers ayant confirmé au moins un vœu pour les spécialités les plus représentées",
        xaxis_title="Année du Baccalauréat",
        yaxis_title="Nombre de candidats",
        template="plotly_dark",
        legend_title="Enseignements de spécialité"
    )
    st.plotly_chart(fig)


    st.write("""
        This scatter plot reveals the relationship between the number of candidates making wishes and those receiving admission offers 
        for each subject combination. Each point represents a subject combination, with its size indicating the number of accepted admissions.
    """)

    # Chapter 4: Popular Formations
    st.header("Part 4: Popular Formations")

    top_formations_wishes = df_detailed.groupby('Formation')['Nombre de candidats bacheliers ayant confirmé au moins un vœu'].sum().nlargest(10)
    top_formations_proposals = df_detailed.groupby('Formation')['Nombre de candidats bacheliers ayant reçu au moins une proposition d\'admission'].sum().nlargest(10)
    top_formations_accepted = df_detailed.groupby('Formation')['Nombre de candidats bacheliers ayant accepté une proposition d\'admission'].sum().nlargest(10)

    top_formations = pd.Index(top_formations_wishes.index).union(top_formations_proposals.index).union(top_formations_accepted.index)

    df_evolution = pd.DataFrame({
        'Formation': top_formations,
        'Confirmed Wishes': df_detailed.groupby('Formation')['Nombre de candidats bacheliers ayant confirmé au moins un vœu'].sum().reindex(top_formations).values,
        'Admission Proposals': df_detailed.groupby('Formation')['Nombre de candidats bacheliers ayant reçu au moins une proposition d\'admission'].sum().reindex(top_formations).values,
        'Accepted Admissions': df_detailed.groupby('Formation')['Nombre de candidats bacheliers ayant accepté une proposition d\'admission'].sum().reindex(top_formations).values
    })

    df_melted = df_evolution.melt(id_vars='Formation', value_vars=['Confirmed Wishes', 'Admission Proposals', 'Accepted Admissions'], 
                                var_name='Stage', value_name='Count')

    fig_bar_animation = px.bar(df_melted, 
                            x='Formation', 
                            y='Count', 
                            color='Formation',
                            animation_frame='Stage',
                            title="Top 15 Formations by Confirmed Wishes, Admission Proposals, and Accepted Admissions",
                            labels={'Count': 'Number of Students', 'Formation': 'Formation'},
                            range_y=[0, df_melted['Count'].max()])

    fig_bar_animation.update_layout(transition_duration=1000)
    st.plotly_chart(fig_bar_animation, use_container_width=True)




    categories = ["Nombre de candidats bacheliers ayant confirmé au moins un vœu","Nombre de candidats bacheliers ayant reçu au moins une proposition d\'admission","Nombre de candidats bacheliers ayant accepté une proposition d\'admission" ]

    top_formations_per_categorie = set()

    for categorie in categories:
        top_10_for_year = df_detailed.groupby('Formation')[categorie].sum().nlargest(15).index
        top_formations_per_categorie.update(top_10_for_year)

    columns_to_drop = ['Année du Baccalauréat', 'Enseignements de spécialité']
    df_filtered = df_detailed[df_detailed['Formation'].isin(top_formations_per_categorie)]
    df_filtered = df_filtered.drop(columns=columns_to_drop, axis=1)

    df_grouped = df_filtered.groupby('Formation').sum().reset_index()
    st.dataframe(df_grouped)
    plot_data = df_grouped.set_index('Formation')[categories]

    fig = go.Figure()

    for formation in plot_data.index:
        fig.add_trace(go.Scatter(
            x=categories,
            y=plot_data.loc[formation],
            mode='lines+markers',
            name=formation,
            line=dict(width=2)
        ))

    fig.update_layout(
        title="Nombre de candidats bacheliers par catégorie",
        xaxis_title="Catégories",
        yaxis_title="Nombre de candidats",
        template="plotly_dark",
        legend_title="Formations",
        height=1000
    )

    st.plotly_chart(fig)

    st.write("""
        We can remark that LAS (medecine cursus) was created in 2020, explaining the amount of wishes made in 2021 has it has replaced a very important previous formation, PACES.
        This bar chart shows the top 10 formations based on the number of candidates who accepted admission offers. 
        This gives us insight into which programs are most popular among students who have been admitted.
    """)

    df_grouped = df_detailed.groupby('Formation').agg({
        categories[0]: 'sum',
        categories[1]: 'sum',
        categories[2]: 'sum'
    }).reset_index()

    df_grouped['Pourcentage propositions reçues'] = df_grouped[categories[1]]* 100 / df_grouped[categories[0]]
    df_grouped['Pourcentage propositions acceptées'] = df_grouped[categories[2]]* 100 / df_grouped[categories[0]]
    st.write(categories[0])

    df_selected = df_grouped
    df_grouped = df_grouped.drop(columns=[categories[0], categories[1], categories[2]])
    st.dataframe(df_grouped)

    formation_choice = st.selectbox("Select a Formation:", df_selected['Formation'].unique())

    df_selected = df_selected[df_selected['Formation'] == formation_choice]

    labels = ['Wishes', 'Proposals Received', 'Proposals Accepted']
    parents = ['', 'Wishes', 'Proposals Received']
    values = [
        df_selected[categories[0]].values[0], 
        df_selected[categories[1]].values[0], 
        df_selected[categories[2]].values[0]
    ]

    color_discrete_map = {
        'Wishes': '#2ca02c',
        'Proposals Received': '#2ca02c',
        'Student Admitted': '#2ca02c',
        'Proposal never received': '#8B0000', 
        'Refused Admissions': '#8B0000'
    }

    refused_prop = df_selected[categories[0]].values[0]-df_selected[categories[1]].values[0]
    refused_adm = df_selected[categories[1]].values[0]-df_selected[categories[2]].values[0]

    fig = go.Figure(go.Sunburst(
        labels=['Wishes', 'Proposals Received', 'Student Admitted', 'Proposal never received', 'Refused Admissions'],
        parents=['', 'Wishes', 'Proposals Received', 'Wishes', 'Proposals Received'],
        values=[df_selected[categories[0]].values[0], 
                df_selected[categories[1]].values[0], 
                df_selected[categories[2]].values[0],
                refused_prop,
                refused_adm,
                refused_prop],
        textinfo='label+value',
        branchvalues='total',
        marker=dict(colors=[
            color_discrete_map['Wishes'],
            color_discrete_map['Proposals Received'],
            color_discrete_map['Student Admitted'],
            color_discrete_map['Proposal never received'],
            color_discrete_map['Refused Admissions']
        ])
    ))

    
    fig.update_layout(
        title_text="Pourcentage of proposition received and accepted over the number of wishes made.",
        height=600, 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)" 
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write(
        f"In {formation_choice}, out of {values[0]} wishes (100%), "
        f"{values[1]} ({df_selected['Pourcentage propositions reçues'].values[0]:.2f}%) proposals were received, "
        f"and {values[2]} ({df_selected['Pourcentage propositions acceptées'].values[0]:.2f}%) proposals were accepted."
    )


    
    st.write("---")
    st.markdown("© 2024 Thaïs Bordessoul. All rights reserved.")


st.sidebar.markdown("---")
st.sidebar.info("Created by Thaïs Bordessoul")
st.sidebar.info("Student in M1 DAI at EFREI PARIS")

