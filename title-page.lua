function Header(elem)
    if elem.level == 1 then
      title = pandoc.utils.stringify(elem.content)
      return {
        pandoc.RawBlock("latex", "\\clearpage"),
        pandoc.RawBlock("latex", "\\centering"),
        pandoc.RawBlock("latex", "\\Huge\\textbf{" .. title .. "}"),
        pandoc.RawBlock("latex", "\\vspace{1em}"),
        elem
      }
    end
  end
  