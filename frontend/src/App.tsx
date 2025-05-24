import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./pages/Header";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import SignUp from "./pages/SignUp";
import LogIn from "./pages/LogIn";
import Search from "./pages/Search";
import TrackDetail from "./pages/TrackDetail";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />{" "}
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/search" element={<Search />} />
        <Route path="/track/:id" element={<TrackDetail />} />
      </Routes>
    </Router>
  );
}
export default App;
