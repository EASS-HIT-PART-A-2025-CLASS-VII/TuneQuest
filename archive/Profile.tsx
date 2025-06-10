// import styles from "./Profile.module.css";
// import userImage from "@/assets/user-image.webp";
// import { useUser } from "@/contexts/UserContext";

// export default function Profile() {
//   const { user } = useUser();
//   if (!user) return <p>No user logged in.</p>;

//   return (
//     <div className={styles.profileContainer}>
//       <div className={styles.first}>
//         <img
//           src={userImage}
//           alt="User profile"
//           className={styles.userImage}
//           onError={(e) => {
//             e.currentTarget.src = "https://via.placeholder.com/150";
//           }}
//         />
//         <p>Full name: {user.fullName}</p>
//         <p>Username: {user.username}</p>
//         <p>Email: {user.email}</p>
//       </div>
//     </div>
//   );
// }
