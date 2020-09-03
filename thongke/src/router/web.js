import express from "express"
import home from "./../controllers/homeController"
let router = express.Router()

let initRouter = (app)=>{ 
    router.get("/", home.getHome)
    return app.use("/", router)
}
module.exports = initRouter