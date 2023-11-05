import { useState, useEffect, useRef } from "react";
import { fetchGet, fetchPost } from "../utils/APIUtils";
import Prompt from "./Prompt";
import ChatSessionHistory from "./ChatSessionHistory";
import Diagnostics from "./Diagnostics";
import Thinking from "./Thinking";
import Box from "@mui/material/Box";
import { TextField, Button } from "@mui/material";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import InputLabel from "@mui/material/InputLabel";
import Slider from "@mui/material/Slider";
import { Link } from "react-router-dom";
import Checkbox from "@mui/material/Checkbox";

const NEW_CONVERSATION_ID = "NEW";

export default function Main({ sessionManager }) {

  /////////////////////////////// STATE ///////////////////////////////
  const [domainList, setDomainList] = useState([]);
  const [domainID, setDomainID] = useState("");
  const [query, setQuery] = useState("");
  const [prompt, setPrompt] = useState("TBD");
  const [promptDefault, setPromptDefault] = useState("TBD");
  const [promptCustom, setPromptCustom] = useState("");
  const [temp, setTemp] = useState(0.4);
  const [chunks, setChunks] = useState([]);
  const [chunksUsedCount, setChunksUsedCount] = useState(0);
  const [chatHistory, setChatHistory] = useState([]);
  const [conversationID, setConversationID] = useState("NEW");
  const [initialMessage, setInitialMessage] = useState("");
  const [deepSearch, setDeepSearch] = useState(false);
  const [showThinking, setShowThinking] = useState(false);

  console.log("Main --> userID", sessionManager.user.userID, domainID);

  function resetConversation() {
    setConversationID(NEW_CONVERSATION_ID);
    if (initialMessage) setChatHistory([initialMessage]);
    else setChatHistory([]);
    setQuery("");
    setShowThinking(false);
    setChunks([]);
    setChunksUsedCount(0);
  }

  // call only from useEffect on domainID change
  async function setActiveDomain(iDomainID) {
    console.log("setActiveDomain -> setting domain to", iDomainID);
    resetConversation();

    const domainData = await fetchGet(`domain/${iDomainID}`);
    setPromptCustom(domainData.initial_prompt_template);
    let newHistory = [];
    if (domainData.initial_conversation_message) {
      setInitialMessage("AI: " + domainData.initial_conversation_message);
      newHistory.push("AI: " + domainData.initial_conversation_message);
    } else {
      setInitialMessage("");
    }

    setChatHistory(newHistory);
    setPrompt(domainData.initial_prompt_template || promptDefault);
  }

  /////////////////////////////// EFFECTS ///////////////////////////////
  // Main useEffect
  useEffect(() => {
    console.log("useEffect -> Main");

    const getOptions = async () => {
      const p = await fetchGet("prompt");
      setPromptDefault(p.prompt_text);
      setPrompt(p.prompt_text);
      const d = await fetchGet("domain");
      setDomainList(d);
    };

    getOptions();
  }, []);

  // Domain change useEffect
  useEffect(() => {
    console.log("useEffect -> domain", domainID);
    if (domainID) setActiveDomain(domainID);
  }, [domainID, promptDefault]);

  // Session useEffect
  useEffect(() => {
    console.log(
      "useEffect -> Session change, userID",
      sessionManager.user.userID
    );

    if (!domainID && sessionManager.user.domainID)
      setDomainID(sessionManager.user.domainID);

    if (!sessionManager.user.userID) {
      setDomainID("");
      setQuery("");
      setPrompt("");
      setShowThinking(false);
      setChunks([]);
      setChunksUsedCount(0);
      setChatHistory([]);
      setConversationID("NEW");
      setInitialMessage("");
    }

    sessionManager.requireUser();
  }, [sessionManager.user.userID]);

  /////////////////////////////// FORM FUNCTIONS ///////////////////////////////
  const formSubmit = async (e) => {
    e.preventDefault();

    setQuery("");
    setShowThinking(true);
    setChunks([]);
    setChunksUsedCount(0);
    setChatHistory((h) => [...h, "User: " + query]);

    const queryObj = {
      domain_id: domainID,
      query,
      prompt_template: prompt,
      temp,
      user_id: sessionManager.user.userID,
      conversation_id: conversationID,
      deep_search: deepSearch,
    };

    try {
      const response = await fetchPost("answer", queryObj);
      setChatHistory((h) => [...h, "AI: " + response.answer]);
      setConversationID(response.conversation_id);
      setShowThinking(false);
      const responseChunks = Object.values(response.chunks).sort(
        (a, b) => b.score - a.score
      );
      setChunks(responseChunks);
      setChunksUsedCount(response.chunks_used_count);
    } catch (e) {
      setChatHistory((h) => [
        ...h,
        "Sorry, an error occured.  Please try again.",
      ]);
      setShowThinking(false);
    }
  };

  /////////////////////////////// RETURN ///////////////////////////////
  return (
    <Box
      component="form"
      maxWidth={800}
      onSubmit={formSubmit}
      sx={{ mt: 1, margin: "auto" }}
    >
      <FormControl fullWidth>
        <div style={{ display: "flex", paddingBottom: 10 }}>
          <div style={{ flexGrow: 1, paddingRight: 10 }}>
            <InputLabel>Domain</InputLabel>
            <Select
              value={domainList.length > 0 ? domainID : ""}
              label="Domain"
              onChange={(e) => {
                setDomainID(e.target.value);
              }}
              style={{ width: "100%" }}
            >
              {domainList.map((d) => (
                <MenuItem key={d.domain_id} value={d.domain_id}>
                  {d.domain_desc}
                </MenuItem>
              ))}
            </Select>
          </div>
          <div style={{ flexGrow: 0, alignSelf: "center" }}>
            <Link
              style={{ textDecoration: "none" }}
              to="#"
              onClick={() => resetConversation()}
            >
              RESTART SESSION
            </Link>
          </div>
        </div>

        <Prompt
          prompt={prompt}
          setPrompt={setPrompt}
          promptCustom={promptCustom}
          promptDefault={promptDefault}
        />

        <div style={{ display: "flex", paddingTop: 10 }}>
          <div style={{ flexGrow: 1, paddingRight: 10 }}>
            <Slider
              aria-label="Temperature"
              defaultValue={temp}
              valueLabelDisplay="auto"
              step={0.1}
              marks
              min={0}
              max={1}
              onChange={(e) => setTemp(e.target.value)}
            />
          </div>
          <div
            style={{
              flexGrow: 0,
              alignSelf: "center",
              paddingLeft: 10,
            }}
          >
            deep search:
            <Checkbox
              checked={deepSearch}
              onChange={(e) => setDeepSearch(e.target.checked)}
              size="small"
            />
          </div>
        </div>

        <ChatSessionHistory chatHistory={chatHistory} />

        <Thinking show={showThinking} />

        <div style={{ display: "flex" }}>
          <div style={{ flexGrow: 1, paddingRight: 10 }}>
            <TextField
              margin="normal"
              fullWidth
              id="querytitle"
              type="text"
              label=""
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              variant="outlined"
              required
            />
          </div>
          <div style={{}}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              style={{ marginTop: 20 }}
            >
              send
            </Button>
          </div>
        </div>
      </FormControl>
      <br />
      <br />
      <Diagnostics
        conversationID={conversationID}
        chunks={chunks}
        chunksUsedCount={chunksUsedCount}
      />
    </Box>
  );
}
