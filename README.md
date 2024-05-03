# Hotel_RAGbot



Project Overview:

This project aims to develop a conversational AI system called "Hotel Ragbot" dedicated to assisting users with hotel bookings. Utilizing advanced natural language processing techniques, Ragbot comprehends user queries and provides tailored responses focused on hotel-related information. By integrating with databases and external APIs, it retrieves relevant data on hotels, delivering personalized and informative assistance to users. Hotel Ragbot is designed to streamline the hotel booking process and enhance the overall user experience in the realm of hotel accommodations.

Code Overview:

Synthetic Data Generation: The code generates synthetic data for hotels including hotel names, brands, addresses, amenities, and descriptions.
Database Setup: Sets up a PostgreSQL database with pgvector extension to store hotel information and vector embeddings.
Data Processing: Maps abbreviations of amenities to their full names and formats the data for insertion into the database.
Embedding Generation: Utilizes Google Vertex AI embeddings model to generate vector embeddings for the hotel data and store in pgvector
Conversational AI Setup: Sets up a conversational AI system using the Langchain and Vertex AI llm (Gemini-Pro).
Conversational Retrieval Chain: Constructs a conversation chain to handle the retrieval of the most relevant vector documents based on user queries and embeddings associated with each document from the pgvector database of vector embeddings, processing follow-up questions, and managing conversation history and context.
App engine: To deploy the RAGbot as a flask application Flask web application with a single POST endpoint /chat, where you can send a JSON object with a question field to get a response from the Hotel RAGbot. 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.
