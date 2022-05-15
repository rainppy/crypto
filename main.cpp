void Fenjie(ZZ n)
{
	if (ProbPrime(n))
	{
		factor[++total] = n;
		return;
	}
	ZZ a, pr;

	pr = Pollard_rho(n);
	Fenjie(pr);
	Fenjie(n / pr);
}
ZZ Pollard_rho(ZZ n)
{
	ZZ p;//返回的因子
	for (int i = 0;i < 100;i++)
	{
		ZZ a, y, x;
		RandomBits(a, 4);
		a = a % n;
		x = a;
		y = (MulMod(x, x, n) + 1) % n;
		while (true)
		{
			x = (MulMod(x, x, n) + 1) % n;
			y = (MulMod(y, y, n) + 1) % n;
			y = (MulMod(y, y, n) + 1) % n;
			if (x == y)
				break;
			p = GCD(abs(x - y), n);
			if (p != 1)
			{
				cout << "x=" << x << "y=" << y << endl;
				return p;
			}
		}
	}
	return n;
}
