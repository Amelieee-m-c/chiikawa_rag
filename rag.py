from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
# 建立向量庫（只做一次）
def build_db():
    loader = TextLoader("sample.txt", encoding='utf-8')
    docs = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh"#北京人工智能研究院 在國際知名的 MTEB 榜單（評測模型好壞的標準）上長期排名前幾名。
        #看資料元是甚麼就用en英文/zh中文
    )

    db = FAISS.from_documents(split_docs, embeddings)
    db.save_local("db") #向量資料庫只做一次就存檔


# 🔥 載入向量庫（API用）
def load_db():
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh"
    )
    return FAISS.load_local("db", embeddings, allow_dangerous_deserialization=True)
def retrieve(query, k=3):
    db = load_db()

    docs = db.similarity_search(query, k=k)

    context = ""
    for i, doc in enumerate(docs):
        context += f"[資料{i+1}] {doc.page_content}\n"

    return context