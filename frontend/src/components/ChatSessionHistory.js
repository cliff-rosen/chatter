import { useEffect, useRef } from "react";
import Divider from "@mui/material/Divider";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function ChatSessionHistory({ chatHistory }) {
  const containerRef = useRef(null);

  console.log('ChatSessionHistory')
  useEffect(() => {
    const container = containerRef.current;
    container.scrollTop = container.scrollHeight;
  }, [chatHistory]);

  if (chatHistory.length === 0) {
    return <div ref={containerRef}></div>;
  }

  return (
    <div ref={containerRef} style={{ maxHeight: "50vh", overflowY: "auto" }}>
      {chatHistory.map((e, i) => {
        console.log('e', e)
        return (
          <div key={i}>
            <Divider style={{ paddingTop: 5, paddingBottom: 5 }} />
            <div style={{ paddingTop: 5 }}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{e}</ReactMarkdown>
            </div>
          </div>
        )
      }
      )}
      <Divider style={{ paddingTop: 5, paddingBottom: 5 }} />
    </div>
  );
}
