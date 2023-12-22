import { useEffect, useRef, useState } from "react";
import { fetchGet } from "../utils/APIUtils";
import Paper from "@mui/material/Paper";
import { TextField, Button, Container, Grid } from '@mui/material';
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

export default function History({ sessionManager }) {

  const [conversations, setConversations] = useState([])

  const [startDate, setStartDate] = useState('2023-01-01');
  const [endDate, setEndDate] = useState('2023-12-31');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log({ startDate, endDate });
    setConversations([])
    
    const getConversations = async () => {
      var url = `conversations?domain_id=${sessionManager.user.domainID}&start_date=${startDate}&end_date=${endDate}`
      try {
        const data = await fetchGet(url);
        console.log('updated data', data)
        setConversations(data)
      } catch (e) {
        console.log('error retrieving conversations')
      }
    }

    getConversations()

  };


  return (
    <div>
      <Container>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Start Date"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                fullWidth
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="End Date"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                fullWidth
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>

            <Grid item xs={12}>
              <Button type="submit" variant="contained" color="primary">
                Submit
              </Button>
            </Grid>

          </Grid>
        </form>
      </Container>

      <br></br>
        <TableContainer component={Paper}>
        <Table aria-label="conversations">
          <TableHead>
                <TableRow>
                  <TableCell align="left">ID</TableCell>
                  <TableCell align="left">Date</TableCell>
                  <TableCell align="left">Text</TableCell>
                </TableRow>
            </TableHead>
        <TableBody>
          {conversations.map(conversation => (
            <TableRow key={conversation.conversation_id}>
              <TableCell style={{ verticalAlign: "top" }} align="left">
                {conversation.conversation_id}
              </TableCell>
              <TableCell style={{ verticalAlign: "top", "width": 200}} align="left">{conversation.date_time_started}</TableCell>
              <TableCell align="left">{conversation.conversation_text.substring(0, 150)}</TableCell>
              </TableRow>
          ))}
        </TableBody>
        </Table>
        </TableContainer>

    </div>
  );
}
