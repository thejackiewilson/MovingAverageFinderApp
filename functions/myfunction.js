exports.handler = async function (event, context) {
    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Hello from Netlify Function!" }),
    };
  };
  
fetch("/.netlify/functions/myFunction")
.then((response) => response.json())
.then((data) => console.log(data));
