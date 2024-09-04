$server = "VCENTER NAME"
$username = "VCENTER_USER"
$password = "VCENTER_PWD"
Connect-VIServer -Server $server -User $username -Password $password

$categoria = "TAG_CATEGORY" #SET CATEGORY HERE

# IF CATEGORY NOT EXIST CREATE IT
if (-not (Get-TagCategory -Name $categoria -ErrorAction SilentlyContinue)) {
    New-TagCategory -Name $categoria
}

# GET ALL NETWORKS
$virtualNetworks = Get-VirtualNetwork

# ASSIGN TAGS TO NETWORKS
foreach ($vNet in $virtualNetworks) {
    $tagName = $vNet.Name

    # IF TAG NOT EXIST CREATE IT
    if (-not (Get-Tag -Name $tagName -Category $categoria -ErrorAction SilentlyContinue)) {
        New-Tag -Name $tagName -Category $categoria
    }

    # ASSIGN TAG
    New-TagAssignment -Entity $vNet -Tag $tagName
}

# DISCONNECT
Disconnect-VIServer -Server $server -Confirm:$false
