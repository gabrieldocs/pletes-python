import { createBrowserRouter } from "react-router-dom"
import Home from "../modules/Home"
import Intro from "../modules/Intro"
import Dashboard from "../modules/dashboard"
import RedirectClose from "../modules/RedirectClose"

export const router = createBrowserRouter([
    {
        path: '/teste',
        element: <Intro />
    },
    {
        path: '/home',
        element: <Home /> 
    },
    {
        path: '/',
        element: <Dashboard />
    },
    {
        path: '/oauth/callback/',
        element: <RedirectClose />
    },
])
