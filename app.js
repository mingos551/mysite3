const fuelData = {
    propane: {
        name: "プロパン",
        highHeatValue: 50.3224811545823,
        lowHeatValue: 46.6489400302978,
        co2Factor: 0.81712914667223,
        note: ""
    },
    propan_low: {
        name: "プロパン(低圧)",
        highHeatValue: 100.24398636371	,
        lowHeatValue: 92.9261753591589,
        co2Factor: 1.62774730412795,
        note: "換算率0.502"
    },
    butane: {
        name: "ブタン",
        highHeatValue: 49.4321011868969,
        lowHeatValue: 45.8235578002534,
        co2Factor: 0.826578294369651,
        note: ""
    },
    kerosene: {
        name: "灯油",
        highHeatValue: 36.4945180652174,
        lowHeatValue: 34.2683524632391,
        co2Factor: 0.682672738147564,
        note: ""
    },
    lightOil: {
        name: "軽油",
        highHeatValue: 38.0418206289855,
        lowHeatValue: 35.7593113912464,
        co2Factor: 0.714974013318546,
        note: ""
    },
    heavyOilA: {
        name: "A重油",
        highHeatValue: 38.9020593739131,
        lowHeatValue: 36.7235440489739,
        co2Factor: 0.751705405591391,
        note: ""
    },
    cityGas: {
        name: "都市ガス (13A)",
        highHeatValue: 39.9641433589486,
        lowHeatValue: 36.4872628867201,
        co2Factor: 0.557671135633351,
        note: ""
    },
    electricity: {
        name: "電力 (家庭用)",
        highHeatValue: 3.6,
        lowHeatValue: 3.6,
        co2Factor: 0.130555555555556,
        note: ""
    }
};

function populateSelectOptions() {
    const energySelect = document.getElementById("energy");
  
    for (const key in fuelData) {
      const option = document.createElement("option");
      option.value = key;
      option.text = fuelData[key].name;
      energySelect.add(option);
    }
  }
  
  document.getElementById("calculate").addEventListener("click", function () {
    const energy = document.getElementById("energy").value;
    const usage = parseFloat(document.getElementById("usage").value);
    const price = parseFloat(document.getElementById("price").value);
  
    const inputData = fuelData[energy];
  
    const results = [];
  
    for (const key in fuelData) {
      const highHeatEquivalentUsage = usage * inputData.highHeatValue / fuelData[key].highHeatValue;
      const lowHeatEquivalentUsage = usage * inputData.lowHeatValue / fuelData[key].lowHeatValue;
  
      const highHeatEquivalentPrice = price * usage / highHeatEquivalentUsage;
      const lowHeatEquivalentPrice = price * usage / lowHeatEquivalentUsage;

      const co2Emission = inputData.co2Factor * usage;
      const highHeatCo2Emission = highHeatEquivalentUsage * fuelData[key].co2Factor;
      const lowHeatCo2Emission = lowHeatEquivalentUsage * fuelData[key].co2Factor;
      const co2DifferenceHigh = co2Emission - highHeatCo2Emission;
      const co2DifferenceLow = co2Emission - highHeatCo2Emission;
  
      results.push({
        name: fuelData[key].name,
        highHeatUsage: highHeatEquivalentUsage,
        lowHeatUsage: lowHeatEquivalentUsage,
        highHeatPrice: highHeatEquivalentPrice,
        lowHeatPrice: lowHeatEquivalentPrice,
        co2Emission: co2Emission,
        highHeatCo2Emission: highHeatCo2Emission,
        lowHeatCo2Emission: lowHeatCo2Emission,
        co2DifferenceHigh: co2DifferenceHigh,
        co2DifferenceLow: co2DifferenceLow,
    }
  
    localStorage.setItem("results", JSON.stringify(results));
    window.location.href = "result.html";
  });