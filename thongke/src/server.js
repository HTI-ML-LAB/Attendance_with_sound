import express from "express"
import configViewEngine from "./config/viewEngine"
import initRouter from "./router/web"
import connectDB from "./config/connectDB"
import bodyParser from "body-parser"

let app = express()

connectDB();

//Config view enine
configViewEngine(app);

//Enable post data for request
app.use(bodyParser.urlencoded({extended:true, limit :"50mb"}));

initRouter(app)

app.listen(process.env.APP_PORT, process.env.APP_HOST, ()=>{
  console.log(`Running in ${process.env.APP_HOST}:${process.env.APP_PORT}`)
})