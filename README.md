# Pain Annotation in Clinical Notes
Textractor is a web application developed to address the critical need for manual pain annotation in clinical notes. This web app serves as a powerful tool for researchers dedicated to advancing the understanding of pain in healthcare.

### Purpose and Functionality
Textractor enables researchers to effortlessly upload PDF files containing clinical notes, initiating a seamless process that transforms raw textual information into valuable tabular data. The core functionality of the web app centers around facilitating the collaborative efforts of experts who log in to review clinical notes and extract pain scores. This pivotal step in the annotation process allows for the capture of pain-related information from a diverse range of patient narratives.

### Database Integration
The extracted pain scores, coupled with the annotator's identity, are meticulously stored in an organized database. This not only ensures the integrity of the data but also establishes a traceable link between annotations and their respective experts. The significance of this record-keeping becomes apparent as these pain scores metamorphose into ground truth labels, serving as a foundational element for our advanced Natural Language Processing (NLP) pipeline. As Textractor seamlessly integrates with the research workflow, it plays a pivotal role in enhancing the efficiency and accuracy of pain annotation processes. By providing a centralized platform for collaborative annotation, Textractor empowers researchers to delve deeper into the intricate landscape of pain-related information within clinical notes.


# Getting Started with Textractor

## Installation

To get started with Textractor, follow these simple steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/hossein-naseri/textractor.git
    ```

2. Navigate to the project directory:

    ```bash
    cd textractor
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main application:

    ```bash
    python main.py
    ```

    This command will start the TexTRACTOR web application.

2. For converting notes from text to PDF, use the following command:

    ```bash
    python DOC2PDF.py
    ```

    This script facilitates the conversion of text notes to PDF format.

That's it! You are now ready to leverage TexTRACTOR for pain annotation in clinical notes. Explore the web application, annotate pain scores, and contribute to the advancement of healthcare research.
