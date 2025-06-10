import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Header from "./components/common/Header";
import Home from "./pages/home/Home";
import SignUp from "./pages/auth/SignUp";
import Login from "./pages/auth/Login";
import Search from "./pages/music/Search";
import TrackDetails from "./pages/music/TrackDetails";
import ArtistDetails from "./pages/music/ArtistDetails";
import AlbumDetails from "./pages/music/AlbumDetails";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import Companion from "./pages/companion/Companion";
import Favorites from "./pages/user/favorites";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/search" element={<Search />} />
        <Route path="/track/:id" element={<TrackDetails />} />
        <Route path="/artist/:id" element={<ArtistDetails />} />
        <Route path="/album/:id" element={<AlbumDetails />} />
        <Route path="/companion" element={<Companion />} />
        <Route
          path="/favorites"
          element={
            <ProtectedRoute>
              <Favorites />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}
export default App;
