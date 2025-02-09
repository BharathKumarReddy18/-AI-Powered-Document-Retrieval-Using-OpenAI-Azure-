🚀 AI-Powered Document Retrieval Using OpenAI & Azure

This project leverages GPT-3.5 Turbo 16K, Azure Vector Search, and SharePoint to build an intelligent document retrieval system. It enables users to search for documents based on semantic similarity, ensuring more accurate and relevant results compared to traditional keyword-based search.

Features
✅ AI-driven semantic search for document retrieval
✅ GPT-3.5 Turbo 16K for generating high-quality embeddings
✅ Azure Vector Search for similarity-based retrieval
✅ SharePoint integration for document storage
✅ Web interface for seamless user experience

Tech Stack
OpenAI GPT-3.5 Turbo 16K – Generates embeddings for similarity search
Azure Vector Search – Enables efficient document retrieval
SharePoint – Used as document storage
Azure Functions (Python) – Backend for processing search queries
HTML, CSS, JavaScript – Frontend for user interaction
Postman – Used to configure data sources, indexes, and skillsets
How It Works
Document Upload – Files are stored in SharePoint
Embedding Generation – GPT-3.5 Turbo 16K creates vector embeddings
Indexing & Storage – Embeddings are stored in Azure Vector Search
User Query – The user searches for a document via the web interface
Semantic Search – The system finds and retrieves the most relevant document based on similarity
Challenges & Learnings
Optimizing embedding-based search for higher accuracy
Fine-tuning Azure Vector Search for faster response times
Enhancing user experience with an intuitive web interface
Setup Instructions
Clone this repository:
sh
Copy
Edit
git clone https://github.com/your-username/your-repo.git
cd your-repo
Install dependencies:
sh
Copy
Edit
pip install -r requirements.txt
Set up Azure Vector Search and SharePoint for document storage
Configure Azure Functions for backend processing
Run the project and start searching documents! 🚀
Contributing
Feel free to contribute by improving search accuracy, UI enhancements, or adding new features!

License
This project is licensed under the MIT License.

