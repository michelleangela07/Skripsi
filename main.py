import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
import numpy as np
import folium
from streamlit_folium import folium_static
import streamlit as st
import plotly.express as px
import io

# Function to load data
def load_data(file):
    data = pd.read_excel(file, engine='openpyxl')  # Use engine='openpyxl' for reading .xlsx files
    return data

# Function to display dataset and download button
def dataset(df, file_name):
    st.write(df)

    # Create a buffer to store the Excel file
    excel_buffer = io.BytesIO()

    # Save the DataFrame to the buffer as an Excel file
    df.to_excel(excel_buffer, index=False, engine="openpyxl")

    # Create a download button
    st.download_button(
        label=f"Unduh {file_name}",
        data=excel_buffer,
        file_name=file_name,
        key=f"download_button_{file_name}"
    )

def generate_map():
    # Membuat peta Pulau Jawa menggunakan folium
    m = folium.Map(location=[-7.6145, 110.7121], zoom_start=7, width=800, height=600)
    #m = folium.Map(location=[-7.6145, 110.7121], zoom_start=7)

    # Menambahkan marker untuk setiap kota dalam cluster 1 (biru)
    cluster_1 = [
        ("Bandung", -6.9147, 107.6098),
        ("Banyumas", -7.5155, 109.2947),
        ("Bekasi", -6.2348, 106.9945),
        ("Blitar", -8.0984, 112.1684),
        ("Bogor", -6.5944, 106.7892),
        ("Cilacap", -7.7188, 109.0159),
        ("Cirebon", -6.7053, 108.5554),
        ("Depok", -6.4025, 106.7942),
        ("Jember", -8.1724, 113.699),
        ("Kediri", -7.8166, 112.0111),
        ("Madiun", -7.6298, 111.5237),
        ("Malang", -7.9666, 112.6326),
        ("Solo", -7.5561, 110.8316),
        ("Sukabumi", -6.9294, 106.9294),
        ("Surabaya", -7.2575, 112.7521),
        ("Surakarta", -7.571, 110.8258)
    ]

    for city, lat, lon in cluster_1:
        popup_content = f"{city}<br>Cluster: 1"
        folium.Marker(location=[lat, lon], popup=popup_content, icon=folium.Icon(color='blue')).add_to(m)

    # Menambahkan marker untuk setiap kota dalam cluster 2 (merah)
    cluster_2 = [
        ("Jakarta Pusat", -6.2088, 106.8456),
        ("Semarang", -7.0051, 110.4381),
        ("Serang", -6.1091, 106.1504),
        ("Tangerang", -6.178, 106.63),
        ("Yogyakarta", -7.7956, 110.3695)
    ]

    for city, lat, lon in cluster_2:
        popup_content = f"{city}<br>Cluster: 2"
        folium.Marker(location=[lat, lon], popup=popup_content, icon=folium.Icon(color='red')).add_to(m)

    # Menambahkan marker untuk setiap kota dalam cluster 3 (hijau)
    cluster_3 = [
        ("Tasikmalaya", -7.3276, 108.2208),
        ("Tegal", -6.8694, 109.1402)
    ]

    for city, lat, lon in cluster_3:
        popup_content = f"{city}<br>Cluster: 3"
        folium.Marker(location=[lat, lon], popup=popup_content, icon=folium.Icon(color='green')).add_to(m)

    return m

# Sidebar
st.sidebar.title("Menu Navigasi")
menu_select = st.sidebar.radio("Menuju ke", ('Halaman Utama', 'Dataset', 'Eksperimen', 'About'))

#Halaman Utama
if menu_select == 'Halaman Utama':
    st.title("Clustering Harga Pangan Pasar Modern Pulau Jawa")
    st.write("Pangan adalah segala sesuatu yang berasal dari sumber baik hayati maupun hewani, baik sudah diolah maupun belum diolah. Pangan memiliki fungsi sebagai sumber makanan dan energi bagi manusia yang oleh sebab itu pangan menjadi salah satu dari kebutuhan pokok manusia yang wajib dipenuhi dalam kehidupan mereka. Jenis pangan sangat beragam beberapa contoh bahan pangan yang sangat umum ditemukan di kalangan masyarakat di antaranya adalah beras, daging ayam, daging sapi, telur ayam, bawang merah, bawang putih, cabai merah keriting, cabai rawit, minyak goreng, dan gula pasir. ")

    st.header("Harga Pangan")
    st.write("Harga pangan di suatu daerah tidak selalu stabil dan sering mengalami perubahan baik penurunan maupun kenaikan harga. Faktor-faktor yang menyebabkan adanya perubahan harga komoditas pangan antara lain adalah gagal panen akibat dari banjir yang merendam lahan pertanian, musim kemarau berkepanjangan yang menyebabkan lahan mengalami kekeringan, atau juga saat menjelang hari raya dimana masyarakat banyak yang membuat acara-acara untuk merayakannya sehingga kebutuhan pangan biasanya semakin meningkat di kalangan masyarakat. Selain itu, harga pangan antar daerah juga beragam dan tidak sama walau berada dalam pulau bahkan provinsi yang sama. ")

    st.header("Penjelasan Percobaan")
    st.write("Pada percobaan ini akan dilakukan pengelompokkan atau clustering harga pangan yang bertujuan untuk mempelajari pola harga pangan di pasar modern Pulau Jawa.")
    df = load_data('ClusterKota.xlsx')
    st.write("Terdapat 23 kota yang berada di dalam Pulau Jawa yang akan dilakukan proses clustering. Kota-kota tersebut adalah seperti yang ditampilkan pada tabel di bawah ini:")
    st.write(df)

    st.header("Peta Cluster di Pulau Jawa")

    # Memanggil fungsi untuk membuat peta dan menampilkannya menggunakan folium_static
    folium_static(generate_map())

    st.header("Hasil Percobaan")
    st.write("Parameter yang digunakan adalah beras, telur ayam, daging ayam, daging sapi, bawang merah, bawang putih, cabai merah keriting, cabai rawit hijau, cabai rawit merah, minyak goreng, dan gula pasir.")

    # Path menuju folder gambar
    image_folder_path = "img"

    # Menentukan teks subheader sesuai pilihan pengguna
    #st.subheader(f"Pola Data Tren {trend_choices} untuk {parameter_choices}")

    # Dropdown untuk memilih cluster
    selected_cluster = st.selectbox("Silahkan Pilih Cluster atau Perbandingan", ["Cluster 1", "Cluster 2", "Cluster 3", "Perbandingan"])

    # Menampilkan gambar sesuai pilihan
    if selected_cluster in ["Cluster 1", "Cluster 2", "Cluster 3"]:
        selected_rg = st.selectbox("Pilih Tren Waktu", ["Tahunan", "Bulanan"], key="tren_waktu")
        selected_pr = st.selectbox("Pilih Parameter", ["Beras", "Telur Ayam", "Daging Ayam", "Daging Sapi", "Bawang Merah", "Bawang Putih", "Cabai Merah Keriting", "Cabai Rawit Hijau", "Cabai Rawit Merah", "Minyak Goreng", "Gula Pasir"], key="parameter")

        cluster_number = selected_cluster[-1]
        trend_suffix = selected_rg.lower()[0]
        image_path = f"C{cluster_number}{trend_suffix}_{selected_pr.lower()}.png" if selected_rg == "Bulanan" else f"C{cluster_number}{trend_suffix}_{selected_pr.lower()}.png"
        st.subheader(f"Pola Data Tren {selected_rg} {selected_pr}")
        st.image(image_path)

    elif selected_cluster == "Perbandingan":
        selected_rgp = st.selectbox("Pilih Tren Waktu", ["Tahunan", "Bulanan"], key="tren_waktu_perbandingan")
        selected_prp = st.selectbox("Pilih Parameter", ["Beras", "Telur Ayam", "Daging Ayam", "Daging Sapi", "Bawang Merah", "Bawang Putih", "Cabai Merah Keriting", "Cabai Rawit Hijau", "Cabai Rawit Merah", "Minyak Goreng", "Gula Pasir"], key="parameter_perbandingan")

        trend_suffixp = selected_rgp.lower()[0]
        image_path = f"P{trend_suffixp}_{selected_prp.lower()}.png"
        #image_path = f"Pt_{selected_prp.lower()}.png"
        st.subheader(f"Perbandingan Pola Data Tren {selected_rgp} {selected_prp}")
        #st.subheader(f"Perbandingan Pola Data Tren {selected_prp}")
        st.image(image_path)

#Eksperimen
elif menu_select == 'Eksperimen':
    st.title("Eksperimen Clustering K-Means")
    uploaded_file = st.file_uploader("Unggah file dengan format xls, xlsx, atau csv", type=["xls", "xlsx", "csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        dft = df.transpose()

        # Menampilkan dataset yang diunggah
        st.write("Di bawah ini merupakan dataset yang diunggah:")
        st.dataframe(dft)

        # Pilihan parameter
        st.header("Parameter Clustering")
        n_clusters = st.slider("Jumlah Cluster", min_value=2, max_value=10, value=3, step=1)
        random_state = st.number_input("Random State", value=0)

        show_silhouette_visualization = st.checkbox("Tampilkan Visualisasi Silhouette", value=True)
        #show_cluster_visualization = st.checkbox("Tampilkan Visualisasi Cluster", value=True)
        show_scatter_plot = st.checkbox("Tampilkan Scatter Plot", value=True)

        # Tombol
        if st.button("Lihat Hasil"):
            # Hitung nilai silhouette untuk jumlah cluster yang dipilih oleh pengguna
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(dft)

            silhouette_avg = silhouette_score(dft, kmeans.labels_)
            sample_silhouette_values = silhouette_samples(dft, kmeans.labels_)

            # Mendapatkan label kluster untuk setiap data point
            labels = kmeans.labels_

            # Mendapatkan posisi centroid dari setiap kluster
            centroids = kmeans.cluster_centers_

            # Tambahkan kolom Cluster ke DataFrame dft
            dft['Cluster'] = kmeans.labels_

            # Tampilkan hanya kolom 'Cluster' pada dataset
            st.subheader("Label Cluster")
            st.write(f"Di bawah ini merupakan tabel label untuk {n_clusters} cluster.")
            cluster_column = dft['Cluster']
            st.write(cluster_column)

            # Menampilkan visualisasi silhouette
            if show_silhouette_visualization:
                st.header("Visualisasi Silhouette")
                fig, ax = plt.subplots()
                y_lower = 10
                for i in range(n_clusters):
                    ith_cluster_silhouette_values = sample_silhouette_values[kmeans.labels_ == i]
                    ith_cluster_silhouette_values.sort()
                    size_cluster_i = ith_cluster_silhouette_values.shape[0]
                    y_upper = y_lower + size_cluster_i
                    color = plt.cm.Spectral(float(i) / n_clusters)
                    ax.fill_betweenx(np.arange(y_lower, y_upper),
                                      0, ith_cluster_silhouette_values,
                                      facecolor=color, edgecolor=color, alpha=0.7)
                    ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
                    y_lower = y_upper + 10
                #ax.set_title("Silhouette Plot")
                #ax.set_xlabel("Silhouette Coefficient Values")
                #ax.set_ylabel("Cluster Label")
                ax.axvline(x=silhouette_avg, color="red", linestyle="--")
                ax.set_yticks([])
                ax.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

                st.pyplot(fig)

                # Menampilkan nilai rata-rata silhouette
                st.write(f"Nilai rata-rata silhouette: {silhouette_avg}")

            ## Menampilkan visualisasi cluster
            #if show_cluster_visualization:
                #st.header("Visualisasi Cluster")
                #fig = px.scatter(dft, x=dft.columns[0], y=dft.columns[1], color='Cluster', hover_name=dft.index,
                          #color_continuous_scale=['blue', 'red'])
                #st.plotly_chart(fig)

            # Menampilkan scatter plot
            if show_scatter_plot:
                st.header("Scatter Plot")
                plt.figure(figsize=(10, 8))
                for i in range(n_clusters):
                    plt.scatter(dft[labels == i].iloc[:, 0], dft[labels == i].iloc[:, 1], label=f'Cluster {i + 1}')
                plt.scatter(centroids[:, 0], centroids[:, 1], c='black', marker='x', label='Centroids')
                plt.title('Scatter Plot of Clusters')
                plt.legend()
                st.pyplot(plt.gcf())

# Dataset
elif menu_select == 'Dataset':
    st.title("Dataset")
    st.write("Dataset yang dapat digunakan dalam eksperimen ini sebaiknya sudah dilakukan proses agregasi fitur. Di bawah ini terdapat dua contoh dataset yang dapat digunakan dalam eksperimen yaitu dataset biasa dan dataset yang sudah melalui proses normalisasi.")

    # Load first dataset
    st.subheader("Dataset Normalisasi")
    st.write("Normalisasi data adalah proses mengubah nilai-nilai dalam sebuah dataset menjadi rentang yang seragam atau standar. Tujuannya adalah untuk menghilangkan anomali, mengurangi redundansi, dan meningkatkan efisiensi analisis data.")
    st.write("Salah satu teknik normalisasi yang umum digunakan adalah Min-Max Scaling. Dalam Min-Max Scaling, nilai-nilai dalam dataset diubah sedemikian rupa sehingga mereka berada dalam rentang tertentu, misalnya antara 0 dan 1.")
    file_name1 = 'TemplateNormalisasi.xlsx'
    df1 = load_data(file_name1)
    dataset(df1, file_name1)

    # Load second dataset
    st.subheader("Dataset Biasa")
    st.write("Dataset ini merupakan dataset yang berisi data sebelum dilakukan proses normalisasi.")
    file_name2 = 'TemplateBiasa.xlsx'
    df2 = load_data(file_name2)
    dataset(df2, file_name2)

#About
elif menu_select == 'About':
    st.title("About")
    #st.write("Welcome to the About Page!")

    st.header("Tentang Program")
    st.write("Ini merupakan sebuah program yang dirancang untuk memenuhi tugas akhir saya sebagai mahasiswa tingkat akhir yang saat ini sedang berkuliah di Universitas Tarumanagara jurusan Teknik Informatika angkatan 2020. Topik tugas akhir yang saya ambil adalah Clustering Harga Pangan di Pasar Modern Pulau Jawa Menggunakan K-Means. Program ini juga dibuat dengan tujuan untuk memberikan informasi seputar harga pangan kepada masyarakat di Pulau Jawa.")

    st.header("Tujuan dan Manfaat")
    st.write("1.	Mengetahui bagaimana performa algoritma K-Means untuk clustering data harga pangan di pasar modern Pulau Jawa.")
    st.write("2.	Mengetahui seperti apa pola harga pangan di pasar modern Pulau Jawa beberapa tahun terakhir.")
    st.write("3.	Sistem yang dikembangkan diharapkan dapat membantu masyarakat dalam memahami pola harga pangan di pasar modern Pulau Jawa.")

    st.header("Penjelasan Menu")
    st.write("- Pada menu Halaman Utama, pengguna dapat melihat hasil dari percobaan clustering yang telah dilakukan.")
    st.write("- Pada menu Dataset, pengguna dapat melihat contoh dataset yang dapat diunduh dan digunakan untuk eksperimen clustering.")
    st.write("- Pada menu Eksperimen, pengguna dapat mengunggah dataset yang telah dipersiapkan dengan menekan tombol BROWSE FILE lalu memilih parameter clustering yang diinginkan. Setelah itu tekan tombol LIHAT HASIL untuk melakukan proses clustering dan menampilkan hasil dari clustering tersebut.")
    st.write("- Pada menu About, pengguna dapat melihat penjelasan singkat tentang program, penjelasan menu, dan tentang perancang.")

    st.header("Tentang Perancang")
    st.write("Di bawah ini merupakan identitas diri saya selaku perancang program ini.")
    ## Path menuju gambar lokal
    #image_path = "profilMichelle.jpg"
    ## Tampilkan gambar
    #st.image(image_path, width=200)
    st.write("<b>Nama Lengkap:</b> Michelle Angela Thena", unsafe_allow_html=True)
    st.write("<b>Universitas Asal:</b> Universitas Tarumanagara", unsafe_allow_html=True)
    st.write("<b>NIM:</b> 535200020", unsafe_allow_html=True)
    st.write("<b>Fakultas:</b> Teknologi Informasi", unsafe_allow_html=True)
    st.write("<b>Jurusan:</b> Teknik Informatika", unsafe_allow_html=True)
