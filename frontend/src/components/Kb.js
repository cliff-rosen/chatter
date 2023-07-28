import { useState } from "react";
import { fetchGet, fetchPost } from "../utils/APIUtils";

export default function Kb({ sessionManager }) {
  const [selectedFile, setSelectedFile] = useState(null);

  const onChangeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(selectedFile);
    const data = new FormData();
    data.append("file", selectedFile);
    const res = await fetchPost("document", data, true);
    console.log(res);
  };

  return (
    <div>
      <h2>File Input Form</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={onChangeHandler} />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
