interface SectionTitleProps {
  title: string;
  subtitle?: string;
  center?: boolean;
}

const SectionTitle = ({ title, subtitle, center = true }: SectionTitleProps) => (
  <div className={`mb-12 ${center ? "text-center" : ""}`}>
    <h2 className="text-3xl md:text-4xl font-heading font-bold mb-3">
      {title}
    </h2>
    {subtitle && (
      <p className="text-muted-foreground max-w-2xl mx-auto text-lg">
        {subtitle}
      </p>
    )}
    <div className={`mt-4 h-1 w-20 rounded-full gradient-bg ${center ? "mx-auto" : ""}`} />
  </div>
);

export default SectionTitle;
