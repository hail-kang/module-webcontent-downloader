class SelectorCommand:
  """
  다운로더의 매개변수로 사용되는 클래스.
  다운로드할 목록이나 이미지는 HTML안에서 URL주소를 가지며, 
  이 URL주소를 얻어내기 위해 선택자를 사용함.
  """
  
  def __init__(self, element, attribute):
    self.element = element
    self.attribute = attribute