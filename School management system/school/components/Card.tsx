interface CardProps {
  title: string;
  description: string;
  image?: string;
}

export default function Card({ title, description, image }: CardProps) {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 hover:shadow-xl transition">
      {image && <img src={image} alt={title} className="rounded-lg mb-4" />}
      <h3 className="font-bold text-lg mb-2">{title}</h3>
      <p>{description}</p>
    </div>
  );
}