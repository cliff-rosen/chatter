import { useEffect, useRef, useState } from "react";
import { fetchGet } from "../utils/APIUtils";

export default function History({ sessionManager }) {

  const [conversations, setConversations] = useState([])


  useEffect(() => {

    const getConversations = async () =>{
      var url = `conversations?domain_id=${sessionManager.user.domainID}&start_date=2023-10-01&end_date=2023-11-01`
      try {
        const data = await fetchGet(url);
        setConversations(data)
      } catch (e) {
        console.log('error retrieving conversations')
      }
    }

    getConversations()
  }, []);


  return (
    <div>
        HISTORY
        {conversations.map(conversation => (
        <div style={{display: 'flex', padding: 10}}>
          <div style={{flex: 1}} id={conversation.conversation_id}>{conversation.conversation_id}</div>
          <div style={{flex: 5}}>{conversation.conversation_text.substring(0, 150)}</div>
        </div>))}
    </div>
  );
}
