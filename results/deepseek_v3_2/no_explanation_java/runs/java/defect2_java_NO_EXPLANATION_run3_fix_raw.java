    public Paint getPaint(double value) {
        double v = Math.max(value, this.lowerBound);
        v = Math.min(v, this.upperBound);
        double proportion = (v - this.lowerBound) / (this.upperBound - this.lowerBound);
        int g = (int) (proportion * 255.0);
        return new Color(g, g, g);
    }