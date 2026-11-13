const MEAN = [170.314, 81.474, 3.141, 62.64, 8.841185452284554, 8.359356172889843];
const STD = [29.125682893281667, 52.32505445768789, 1.7863703423422634, 33.52399737501482, 6.373795483485292, 2.3137340758188687];
const COEF = [-0.5714266759905501, 0.7683295801865215, -0.8533674608717052, 0.8314139870118136, -4.353675088236089, 0.3368004018309106];
const INTERCEPT = 0.09514686391034788;
function winProb(vals){
  let z = INTERCEPT;
  for (let i = 0; i < 6; i++) z += COEF[i] * (vals[i] - MEAN[i]) / STD[i];
  return 1 / (1 + Math.exp(-z)) * 100;
}
function fullRow(target, runs, wkts, ballsLeft){
  const ballsBowled = 120 - ballsLeft;
  const rrr = (target - runs) / Math.max(ballsLeft / 6, 0.5);
  const crr = runs / Math.max(ballsBowled / 6, 0.5);
  return [target, runs, wkts, ballsLeft, rrr, crr];
}
console.log(JSON.stringify({row: [180, 150, 3, 30, 6.0, 10.0], js: winProb([180, 150, 3, 30, 6.0, 10.0]), py: 91.28323357868715}));
console.log(JSON.stringify({row: [180, 90, 7, 60, 9.0, 9.0], js: winProb([180, 90, 7, 60, 9.0, 9.0]), py: 13.080345587037536}));
console.log(JSON.stringify({row: [160, 110, 4, 36, 8.333333333333334, 7.857142857142857], js: winProb([160, 110, 4, 36, 8.333333333333334, 7.857142857142857]), py: 47.97904626060301}));
console.log(JSON.stringify({row: [200, 60, 2, 90, 9.333333333333334, 12.0], js: winProb([200, 60, 2, 90, 9.333333333333334, 12.0]), py: 64.90362576643301}));
console.log(JSON.stringify({row: [150, 145, 8, 12, 2.5, 8.055555555555555], js: winProb([150, 145, 8, 12, 2.5, 8.055555555555555]), py: 89.4407941790893}));