class Line < ActiveRecord::Base
  set_table_name 'slines'
  belongs_to :sombyl
  has_many :points

  def before_destroy
    @points = Point.find(:all, :conditions=>{ :line_id=>self.id })
    @points.each do |p|
      p.destroy
    end

  end
end
