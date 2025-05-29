import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Home from "./pages/Home";
import Profile from "./pages/Profile";
import SignUp from "./pages/SignUp";
import LogIn from "./pages/LogIn";
import Search from "./pages/Search";
import TrackDetails from "./pages/TrackDetails";
import ArtistDetails from "./pages/ArtistDetails";
import AlbumDetails from "./pages/AlbumDetails";
import ProtectedRoute from "./components/ProtectedRoute";
import Companion from "./pages/Companion";

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
        <Route path="/track/:id" element={<TrackDetails />} />
        <Route path="/artist/:id" element={<ArtistDetails />} />
        <Route path="/album/:id" element={<AlbumDetails />} />
        <Route path="/companion" element={<Companion />} />
      </Routes>
    </Router>
  );
}
export default App;
