import { ReactNode } from "react";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

const GlassCard = ({ children, className = "", hover = true, onClick }: GlassCardProps) => (
  <div className={`glass ${hover ? "hover-lift" : ""} ${className}`} onClick={onClick}>
    {children}
  </div>
);

export default GlassCard;
