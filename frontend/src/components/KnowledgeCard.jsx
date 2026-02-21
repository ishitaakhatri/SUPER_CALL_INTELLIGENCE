export default function KnowledgeCard({ docs }) {
    if (!docs || docs.length === 0) {
        return (
            <div className="card knowledge empty">
                <div className="empty-state">
                    <div className="empty-icon">📚</div>
                    <h3>Knowledge Articles</h3>
                    <p>Relevant policy documents will appear here</p>
                </div>
            </div>
        );
    }

    return (
        <div className="card knowledge">
            <div className="card-header">
                <div className="card-icon">📚</div>
                <div>
                    <div className="card-title">Knowledge Articles</div>
                    <div className="card-subtitle">{docs.length} relevant document{docs.length !== 1 ? 's' : ''} found</div>
                </div>
            </div>
            <div className="card-body">
                {docs.map((doc) => (
                    <div key={doc.docId} className="knowledge-article">
                        <div className="doc-id">{doc.docId}</div>
                        <h4>{doc.title}</h4>
                        <p>{doc.content}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
