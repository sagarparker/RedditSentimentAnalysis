import './App.css';
import {React,useState} from 'react'
import axios from 'axios'

function App() {
  const [sentence,setSentence] = useState("");
  const [sentimentResult,setSentimentResult] = useState("");

  //Get the predicted sentiment result from the flask server
  const getSentiment = (event) => {
    event.preventDefault();
    axios.post('http://127.0.0.1:5000/getPrediction',{
      "post":sentence
    },{ validateStatus: false })
    .then((response)=>{
      setSentimentResult(response.data[0])
      console.log(sentimentResult)
    })
    .catch((err)=>{
      console.log(err);
    })
  }

  return (
    <div className="mainDiv">
    <nav class="navbar navbar-light bg-light">
    <div class="container-fluid">
      
      <span class="navbar-brand mb-0 h1"><img src="reddit.png" width="30" style={{marginTop:-3,marginRight:7}} height="30" alt=""/>Reddit post sentiment analysis</span>
    </div>
    </nav>
    <div className="App">

      <div className="formHolder">
          <form onSubmit={getSentiment}>
            <input required type="text" autoComplete="false" name="posttext" id="inputField" placeholder="Please enter a post to predict the sentiment" value={sentence} onChange={(e)=>setSentence(e.target.value)}/>
            <button type="submit" id="submitBtn">Predict</button>
          </form>
          {
            (sentimentResult === 1) ?
            <img src="smiling.svg" width="200" height="200" alt="smiling"/>
            :
            (sentimentResult === 0)?
            <img src="neutral.svg" width="200" height="200" alt="neutral"/>
            :
            (sentimentResult === -1)?
            <img src="sad.svg" width="200" height="200" alt="sad"/>
            :
            <h5 style={{color:'white',fontSize:'20px'}}>Please enter a post above to get a result</h5>
          }
      </div>
    </div>
    </div>
  );
}

export default App;
