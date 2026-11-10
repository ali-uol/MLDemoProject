const species = [
  [
    "01",
    "Iris Setosa",
    "Small petals with a distinctive shape; often separates clearly from the other two species.",
  ],
  [
    "02",
    "Iris Versicolor",
    "Intermediate petal measurements that can overlap with Virginica.",
  ],
  [
    "03",
    "Iris Virginica",
    "Typically longer and wider petals, with some variation between individual flowers.",
  ],
];
export default function SpeciesCard() {
  return (
    <section className="species-grid" aria-label="About the species">
      {species.map(([number, name, text]) => (
        <article className="species-card" key={name}>
          <span className="eyebrow">SPECIES {number}</span>
          <h3>{name}</h3>
          <p>{text}</p>
        </article>
      ))}
    </section>
  );
}
