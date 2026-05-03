import { useEffect, useState } from "react";
import { View, Text, FlatList } from "react-native";

export default function Home() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    fetch("http://192.168.1.22:5000/matches")
      .then(res => res.json())
      .then(data => setMatches(data))
      .catch(err => console.log(err));
  }, []);

  const renderMatch = ({ item }) => {
    const isHot = item.decision === "NEXT GOAL";
    const isBad = item.decision === "NO BET";

    return (
      <View
        style={{
          margin: 10,
          padding: 15,
          borderRadius: 15,
          borderWidth: 2,
          borderColor: isHot ? "lime" : isBad ? "red" : "gray",
          backgroundColor: "#111"
        }}
      >
        <Text style={{ color: "white", fontSize: 18 }}>
          {item.home} vs {item.away}
        </Text>

        <Text style={{ color: "white" }}>Score: {item.score}</Text>
        <Text style={{ color: "white" }}>Minute: {item.minute}</Text>

        <Text style={{ color: "cyan" }}>📊 Shots: {item.shots}</Text>
        <Text style={{ color: "cyan" }}>📈 xG: {item.xg}</Text>

        <Text style={{ color: "orange" }}>
          🎯 Goal Probability: {item.prob_goal}%
        </Text>

        <Text style={{ color: "yellow" }}>
          ⚡ Intensity: {item.intensity}
        </Text>

        <Text style={{ color: "gold" }}>
          💰 Value: {item.value}
        </Text>

        <Text
          style={{
            color: isHot ? "lime" : isBad ? "red" : "white",
            fontSize: 20,
            marginTop: 10
          }}
        >
          🔥 {item.decision}
        </Text>

        <Text style={{ color: "white" }}>
          🎯 Confidence: {item.confidence}%
        </Text>

        <Text style={{ color: "gray" }}>
          🧠 {item.reason}
        </Text>
      </View>
    );
  };

  return (
    <View style={{ flex: 1, backgroundColor: "black", paddingTop: 50 }}>
      <Text style={{ color: "white", fontSize: 22, textAlign: "center" }}>
        ⚽ AI BETTING ELITE 🔥
      </Text>

      <FlatList
        data={matches}
        renderItem={renderMatch}
        keyExtractor={(item, index) => index.toString()}
      />
    </View>
  );
}