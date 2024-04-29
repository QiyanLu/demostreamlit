import streamlit as st
import requests
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import molecular_weight
from Bio.Align.Applications import ClustalOmegaCommandline

# Function to retrieve protein data from Uniprot ID
def fetch_protein_data(uniprot_id):
    # Use Uniprot API to get protein data
    url = f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to retrieve protein-protein interaction network from STRING DB
def fetch_ppi_network(uniprot_id):
    # Implement retrieval from STRING DB
    pass

# Main function to run the Streamlit app
def main():
    st.title("Protein Study App")
    st.sidebar.title("Options")

    option = st.sidebar.selectbox("Choose an option", ("By Uniprot ID", "By Protein Sequence"))

    if option == "By Uniprot ID":
        uniprot_id = st.sidebar.text_input("Enter Uniprot ID")
        if st.sidebar.button("Fetch Data"):
            protein_data = fetch_protein_data(uniprot_id)
            if protein_data:
                st.write("## Protein Characteristics")
                st.write(f"Protein ID: {protein_data['accession']}")
                st.write(f"Protein Name: {protein_data['protein']['recommendedName']['fullName']['value']}")
                st.write(f"Protein Length: {protein_data['sequence']['length']}")
                st.write(f"Protein Weight: {molecular_weight(Seq(protein_data['sequence']['sequence']), "protein"):.2f} kDa")

                st.write("## Protein-Protein Interaction Network")
                # Call function to fetch PPI network and display here

    elif option == "By Protein Sequence":
        uploaded_file = st.sidebar.file_uploader("Upload Protein Sequence (FASTA format)")
        if uploaded_file is not None:
            protein_seq = SeqIO.read(uploaded_file, "fasta")
            st.write("### Uploaded Protein Sequence")
            st.write(f"Sequence ID: {protein_seq.id}")
            st.write(f"Sequence Length: {len(protein_seq)}")
            st.write(f"Sequence: {protein_seq.seq}")

            # Implement analysis of protein sequence
            st.write("## Sequence Alignment Output")
            # Use Clustal Omega for sequence alignment
            clustalomega_cline = ClustalOmegaCommandline(infile=uploaded_file.name, outfile="aligned.fasta", verbose=True, auto=True)
            stdout, stderr = clustalomega_cline()
            alignment = SeqIO.read("aligned.fasta", "fasta")
            st.write(alignment)

if __name__ == "__main__":
    main()
