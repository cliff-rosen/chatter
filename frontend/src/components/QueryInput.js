import { useState } from "react";
import { TextField, Button } from "@mui/material";

export default function QueryInput({ formSubmit }) {

    const [iquery, setIquery] = useState("");

    console.log('MyInput')


    function iFormSubmit(e) {
        e.preventDefault();
        setIquery("")
        formSubmit(iquery)
    }

    return (
        <div style={{ display: "flex" }}>
            <div style={{ flexGrow: 1, paddingRight: 10 }}>
                <TextField
                    margin="normal"
                    fullWidth
                    id="querytitle"
                    type="text"
                    label=""
                    value={iquery}
                    onChange={(e) => setIquery(e.target.value)}
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
                    onClick={iFormSubmit}
                >
                    send
                </Button>
            </div>
        </div>

    );
}
