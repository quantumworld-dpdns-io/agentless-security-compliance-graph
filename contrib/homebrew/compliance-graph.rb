class ComplianceGraph < Formula
  desc "Agentless Security Compliance Graph — map devices, AD accounts, CVEs, and policy gaps"
  homepage "https://github.com/quantumworld-dpdns-io/agentless-security-compliance-graph"
  url "https://github.com/quantumworld-dpdns-io/agentless-security-compliance-graph/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  license "MIT"

  depends_on "python@3.12"

  def install
    system "pip3", "install", "--prefix=#{prefix}", "-e", "."
    bin.install "bin/agentless-discovery" if File.exist?("bin/agentless-discovery")
  end

  test do
    system "#{bin}/compliance-graph", "--help"
  end
end
