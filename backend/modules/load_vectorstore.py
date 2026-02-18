import os
import time
from pathlib import Path
from dotenv import load_dotenv # type: ignore
from tqdm.auto import tqdm # type: ignore
from pinecone import Pinecone, ServerlessSpec # type: ignore
from langchain_community.document_loaders import PyPDFLoader # type: ignore
from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore
from langchain_google_genai import GoogleGenerativeAIEmbeddings # type: ignore

# from google import genai

# client = genai.Client(api_key="GOOGLE_API_KEY")

# for model in client.models.list():
#     print(model.name)


#Below function is used to load all the environment variables
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
# As we are using pinecone free tier so it will give AWS as the cloud source provider and gives the us-east region by default for the free-tiers
PINECONE_ENV="us-east-1"
PINECONE_INDEX_NAME="indexmedical"

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

UPLOAD_DIR="./uploaded_docs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

#initializing the pinecone instance for pinecone vector db
pc=Pinecone(api_key=PINECONE_API_KEY)
spec=ServerlessSpec(cloud="aws",region=PINECONE_ENV)
existing_indexes=[i["name"]for i in pc.list_indexes()]

# Below function is to create a index
if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        # The `dimension=3072` parameter in the `pc.create_index` function call is specifying the
        # dimensionality of the vectors that will be stored in the Pinecone index. In this case, it is
        # setting the dimensionality of the vectors to 3072. This means that each vector stored in the
        # index will have 3072 dimensions. This dimensionality is important for various operations
        # such as similarity calculations and nearest neighbor searches within the vector space.
        dimension=3072,
        metric="dotproduct",
        spec=spec
    )
    #Below while loop is to give some rest to our embedding model so untill the index is created
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)
index=pc.Index(PINECONE_INDEX_NAME)

#load, split, embed the healthcare pdf docs
def load_vectorstore(uploaded_files):
    embed_model=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    file_paths=[]
    
    #1. upload the datasets
    for file in uploaded_files:
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path,"wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))
        
    #2. split the datasets
    for file_path in file_paths:
        loader=PyPDFLoader(file_path)
        documents=loader.load()
        
        # now split th files into chunks/chunking the files into smaller documents
        splitter=RecursiveCharacterTextSplitter(chunk_size=550,chunk_overlap=100)
        chunks=splitter.split_documents(documents)
        
        texts=[chunk.page_content for chunk in chunks]
        metadata=[chunk.metadata for chunk in chunks]
        ids=[f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]
        
        # Embedding the datasets
        print(f"Embedding chunks/documents")
        #now embedding variable will contain the embedded vectors
        embedding=embed_model.embed_documents(texts)
        
        # Upsert the embedded vectors to the pinecone database
        print(f"📤 Upserting the embedded vectors into the pinecone database")
        with tqdm(total=len(embedding), desc="Upserting to Pinecone") as progress:
            index.upsert(vectors=zip(ids, embedding, metadata))
            progress.update(len(embedding))
            
        print(f"✅ Successfully upserting {len(embedding)} vectors for {file_path} into Pinecone index '{PINECONE_INDEX_NAME}'")