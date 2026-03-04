interface SectionTitleProps {
  title: string;
}

export default function SectionTitle({ title }: SectionTitleProps) {
  return (
    <h2 className="text-3xl font-bold text-primary mb-4">{title}</h2>
  );
}